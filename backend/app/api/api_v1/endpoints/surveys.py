# backend/app/api/api_v1/endpoints/surveys.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.core.database import get_db
from app.api.api_v1.endpoints.auth import get_current_active_user, get_current_admin_user, get_current_coordinator_user
from app.models.user import User, Survey, Question
from app.schemas.survey import (
    SurveyCreate, SurveyUpdate, SurveyResponse, SurveyList, SurveyWithQuestions,
    QuestionCreate, QuestionUpdate, QuestionResponse
)

router = APIRouter()

@router.get("/", response_model=SurveyList)
async def get_surveys(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(20, ge=1, le=100, description="Límite de registros"),
    search: Optional[str] = Query(None, description="Buscar por título o descripción"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    created_by: Optional[str] = Query(None, description="Filtrar por creador"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_coordinator_user)  # Coordinador+ puede ver encuestas
):
    """
    Obtener lista de encuestas con filtros, búsqueda y paginación
    """
    # Query base
    query = db.query(Survey)
    
    # Filtros por rol del usuario actual
    if not current_user.is_admin:
        # Coordinadores solo ven encuestas que crearon ellos o las públicas
        query = query.filter(
            or_(
                Survey.created_by == current_user.id,
                Survey.created_by.is_(None)  # Encuestas públicas/del sistema
            )
        )
    
    # Búsqueda por texto
    if search:
        search_filter = or_(
            Survey.title.ilike(f"%{search}%"),
            Survey.description.ilike(f"%{search}%"),
            Survey.instructions.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Filtro por estado activo
    if is_active is not None:
        query = query.filter(Survey.is_active == is_active)
    
    # Filtro por creador
    if created_by:
        query = query.filter(Survey.created_by == created_by)
    
    # Contar total antes de paginar
    total = query.count()
    
    # Aplicar paginación y ordenamiento
    surveys = query.order_by(Survey.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "surveys": surveys,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total
    }

@router.get("/{survey_id}", response_model=SurveyWithQuestions)
async def get_survey(
    survey_id: str,
    include_questions: bool = Query(True, description="Incluir preguntas de la encuesta"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener una encuesta específica por ID con sus preguntas
    """
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Encuesta no encontrada"
        )
    
    # Verificar permisos
    if not current_user.is_admin:
        if current_user.is_coordinator:
            # Coordinador solo puede ver encuestas que creó o públicas
            if survey.created_by != current_user.id and survey.created_by is not None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para ver esta encuesta"
                )
        elif current_user.is_teacher:
            # Maestros solo pueden ver encuestas activas (para responder)
            if not survey.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Esta encuesta no está disponible"
                )
    
    return survey

@router.post("/", response_model=SurveyResponse)
async def create_survey(
    survey_data: SurveyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_coordinator_user)  # Coordinador+ puede crear
):
    """
    Crear una nueva encuesta
    """
    # Verificar que no existe una encuesta con el mismo título del mismo creador
    existing_survey = db.query(Survey).filter(
        Survey.title == survey_data.title,
        Survey.created_by == current_user.id
    ).first()
    
    if existing_survey:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya tienes una encuesta con este título"
        )
    
    # Crear la encuesta
    db_survey = Survey(
        title=survey_data.title,
        description=survey_data.description,
        instructions=survey_data.instructions,
        is_active=survey_data.is_active,
        created_by=current_user.id
    )
    
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    
    # Crear preguntas si se proporcionaron
    if survey_data.questions:
        for i, question_data in enumerate(survey_data.questions):
            db_question = Question(
                survey_id=db_survey.id,
                question_text=question_data.question_text,
                question_type=question_data.question_type,
                order_number=i + 1,
                is_required=question_data.is_required,
                min_value=question_data.min_value,
                max_value=question_data.max_value,
                # options=question_data.options
            )
            db.add(db_question)
        
        db.commit()
    
    return db_survey

@router.put("/{survey_id}", response_model=SurveyResponse)
async def update_survey(
    survey_id: str,
    survey_data: SurveyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualizar una encuesta existente
    """
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Encuesta no encontrada"
        )
    
    # Verificar permisos
    can_edit = False
    if current_user.is_admin:
        can_edit = True
    elif current_user.is_coordinator and survey.created_by == current_user.id:
        can_edit = True
    
    if not can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar esta encuesta"
        )
    
    # Actualizar campos
    update_data = survey_data.dict(exclude_unset=True)
    
    # Verificar título único si se está cambiando
    if "title" in update_data and update_data["title"] != survey.title:
        existing_survey = db.query(Survey).filter(
            Survey.title == update_data["title"],
            Survey.created_by == survey.created_by,
            Survey.id != survey_id
        ).first()
        
        if existing_survey:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya tienes una encuesta con este título"
            )
    
    # Aplicar actualizaciones
    for field, value in update_data.items():
        if field != "questions":  # Las preguntas se manejan por separado
            setattr(survey, field, value)
    
    db.commit()
    db.refresh(survey)
    
    return survey

@router.delete("/{survey_id}")
async def delete_survey(
    survey_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Eliminar una encuesta (soft delete - desactivar)
    """
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Encuesta no encontrada"
        )
    
    # Verificar permisos
    can_delete = False
    if current_user.is_admin:
        can_delete = True
    elif current_user.is_coordinator and survey.created_by == current_user.id:
        can_delete = True
    
    if not can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar esta encuesta"
        )
    
    # Verificar que no esté siendo usada en evaluaciones
    # TODO: Agregar verificación cuando implementemos evaluaciones
    
    # Soft delete - desactivar
    survey.is_active = False
    db.commit()
    
    return {"message": "Encuesta desactivada exitosamente"}

@router.patch("/{survey_id}/toggle-status")
async def toggle_survey_status(
    survey_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Activar/desactivar una encuesta
    """
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Encuesta no encontrada"
        )
    
    # Verificar permisos
    can_toggle = False
    if current_user.is_admin:
        can_toggle = True
    elif current_user.is_coordinator and survey.created_by == current_user.id:
        can_toggle = True
    
    if not can_toggle:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para cambiar el estado de esta encuesta"
        )
    
    survey.is_active = not survey.is_active
    db.commit()
    
    status_text = "activada" if survey.is_active else "desactivada"
    return {"message": f"Encuesta {status_text} exitosamente", "is_active": survey.is_active}

# ===== ENDPOINTS DE PREGUNTAS =====

@router.get("/{survey_id}/questions", response_model=List[QuestionResponse])
async def get_survey_questions(
    survey_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener todas las preguntas de una encuesta
    """
    # Verificar que la encuesta existe y el usuario tiene permisos
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Encuesta no encontrada"
        )
    
    # Verificar permisos (mismo que get_survey)
    if not current_user.is_admin:
        if current_user.is_coordinator:
            if survey.created_by != current_user.id and survey.created_by is not None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para ver esta encuesta"
                )
        elif current_user.is_teacher:
            if not survey.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Esta encuesta no está disponible"
                )
    
    questions = db.query(Question).filter(
        Question.survey_id == survey_id
    ).order_by(Question.order_number).all()
    
    return questions

@router.post("/{survey_id}/questions", response_model=QuestionResponse)
async def create_question(
    survey_id: str,
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Agregar una pregunta a una encuesta
    """
    # Verificar que la encuesta existe y permisos
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Encuesta no encontrada"
        )
    
    # Verificar permisos de edición
    can_edit = False
    if current_user.is_admin:
        can_edit = True
    elif current_user.is_coordinator and survey.created_by == current_user.id:
        can_edit = True
    
    if not can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar esta encuesta"
        )
    
    # Obtener el siguiente número de orden
    max_order = db.query(func.max(Question.order_number)).filter(
        Question.survey_id == survey_id
    ).scalar()
    next_order = (max_order or 0) + 1
    
    # Crear la pregunta
    db_question = Question(
        survey_id=survey_id,
        question_text=question_data.question_text,
        question_type=question_data.question_type,
        order_number=question_data.order_number or next_order,
        is_required=question_data.is_required,
        min_value=question_data.min_value,
        max_value=question_data.max_value,
        # options=question_data.options
    )
    
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    return db_question

@router.put("/{survey_id}/questions/{question_id}", response_model=QuestionResponse)
async def update_question(
    survey_id: str,
    question_id: str,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualizar una pregunta específica
    """
    # Verificar encuesta y pregunta
    question = db.query(Question).filter(
        Question.id == question_id,
        Question.survey_id == survey_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pregunta no encontrada"
        )
    
    # Verificar permisos
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    can_edit = False
    if current_user.is_admin:
        can_edit = True
    elif current_user.is_coordinator and survey.created_by == current_user.id:
        can_edit = True
    
    if not can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar esta pregunta"
        )
    
    # Actualizar campos
    update_data = question_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(question, field, value)
    
    db.commit()
    db.refresh(question)
    
    return question

@router.delete("/{survey_id}/questions/{question_id}")
async def delete_question(
    survey_id: str,
    question_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Eliminar una pregunta de una encuesta
    """
    # Verificar encuesta y pregunta
    question = db.query(Question).filter(
        Question.id == question_id,
        Question.survey_id == survey_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pregunta no encontrada"
        )
    
    # Verificar permisos
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    can_edit = False
    if current_user.is_admin:
        can_edit = True
    elif current_user.is_coordinator and survey.created_by == current_user.id:
        can_edit = True
    
    if not can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar esta pregunta"
        )
    
    # Eliminar la pregunta
    db.delete(question)
    db.commit()
    
    return {"message": "Pregunta eliminada exitosamente"}

@router.patch("/{survey_id}/questions/reorder")
async def reorder_questions(
    survey_id: str,
    question_orders: List[dict],  # [{"question_id": "uuid", "order_number": 1}, ...]
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Reordenar preguntas de una encuesta
    """
    # Verificar encuesta y permisos
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Encuesta no encontrada"
        )
    
    can_edit = False
    if current_user.is_admin:
        can_edit = True
    elif current_user.is_coordinator and survey.created_by == current_user.id:
        can_edit = True
    
    if not can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para reordenar las preguntas"
        )
    
    # Actualizar orden de preguntas
    for item in question_orders:
        question = db.query(Question).filter(
            Question.id == item["question_id"],
            Question.survey_id == survey_id
        ).first()
        
        if question:
            question.order_number = item["order_number"]
    
    db.commit()
    
    return {"message": "Preguntas reordenadas exitosamente"}