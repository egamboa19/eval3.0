

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

# ===== SCHEMAS DE PREGUNTAS =====

class QuestionBase(BaseModel):
    """Schema base de pregunta"""
    question_text: str
    question_type: str = "scale"  # scale, text, multiple_choice, yes_no
    order_number: Optional[int] = None
    is_required: bool = True
    min_value: Optional[int] = 1
    max_value: Optional[int] = 10
    options: Optional[Dict[str, Any]] = None  # Para opciones de multiple choice, etc.

class QuestionCreate(QuestionBase):
    """Schema para crear pregunta"""
    
    @validator('question_text')
    def validate_question_text(cls, v):
        if not v or len(v.strip()) < 5:
            raise ValueError('La pregunta debe tener al menos 5 caracteres')
        return v.strip()
    
    @validator('question_type')
    def validate_question_type(cls, v):
        valid_types = ['scale', 'text', 'multiple_choice', 'yes_no', 'rating']
        if v not in valid_types:
            raise ValueError(f'Tipo de pregunta debe ser uno de: {", ".join(valid_types)}')
        return v
    
    @validator('min_value', 'max_value')
    def validate_scale_values(cls, v, values):
        if values.get('question_type') == 'scale' and v is not None:
            if v < 1 or v > 10:
                raise ValueError('Los valores de escala deben estar entre 1 y 10')
        return v

class QuestionUpdate(BaseModel):
    """Schema para actualizar pregunta"""
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    order_number: Optional[int] = None
    is_required: Optional[bool] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    options: Optional[Dict[str, Any]] = None
    
    @validator('question_text')
    def validate_question_text(cls, v):
        if v and len(v.strip()) < 5:
            raise ValueError('La pregunta debe tener al menos 5 caracteres')
        return v.strip() if v else None
    
    @validator('question_type')
    def validate_question_type(cls, v):
        if v:
            valid_types = ['scale', 'text', 'multiple_choice', 'yes_no', 'rating']
            if v not in valid_types:
                raise ValueError(f'Tipo de pregunta debe ser uno de: {", ".join(valid_types)}')
        return v

class QuestionResponse(BaseModel):
    """Schema para respuesta de pregunta"""
    id: str
    question_text: str
    question_type: str
    order_number: int
    is_required: bool
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    options: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        
    @validator('id', pre=True)
    def convert_uuid_to_string(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

# ===== SCHEMAS DE ENCUESTAS =====

class SurveyBase(BaseModel):
    """Schema base de encuesta"""
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    is_active: bool = True

class SurveyCreate(SurveyBase):
    """Schema para crear encuesta"""
    questions: Optional[List[QuestionCreate]] = []
    
    @validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('El título debe tener al menos 3 caracteres')
        if len(v.strip()) > 255:
            raise ValueError('El título no puede exceder 255 caracteres')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if v and len(v.strip()) > 1000:
            raise ValueError('La descripción no puede exceder 1000 caracteres')
        return v.strip() if v else None
    
    @validator('instructions')
    def validate_instructions(cls, v):
        if v and len(v.strip()) > 2000:
            raise ValueError('Las instrucciones no pueden exceder 2000 caracteres')
        return v.strip() if v else None

class SurveyUpdate(BaseModel):
    """Schema para actualizar encuesta"""
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    is_active: Optional[bool] = None
    
    @validator('title')
    def validate_title(cls, v):
        if v and (not v or len(v.strip()) < 3):
            raise ValueError('El título debe tener al menos 3 caracteres')
        if v and len(v.strip()) > 255:
            raise ValueError('El título no puede exceder 255 caracteres')
        return v.strip() if v else None
    
    @validator('description')
    def validate_description(cls, v):
        if v and len(v.strip()) > 1000:
            raise ValueError('La descripción no puede exceder 1000 caracteres')
        return v.strip() if v else None
    
    @validator('instructions')
    def validate_instructions(cls, v):
        if v and len(v.strip()) > 2000:
            raise ValueError('Las instrucciones no pueden exceder 2000 caracteres')
        return v.strip() if v else None

class SurveyResponse(BaseModel):
    """Schema para respuesta de encuesta"""
    id: str
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    is_active: bool
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
    @validator('id', 'created_by', pre=True)
    def convert_uuids_to_string(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

class SurveyWithQuestions(SurveyResponse):
    """Schema de encuesta con preguntas incluidas"""
    questions: List[QuestionResponse] = []
    
    class Config:
        from_attributes = True

class SurveySummary(BaseModel):
    """Schema resumido de encuesta para listas"""
    id: str
    title: str
    description: Optional[str] = None
    is_active: bool
    question_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        
    @validator('id', pre=True)
    def convert_uuid_to_string(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

class SurveyList(BaseModel):
    """Schema para lista paginada de encuestas"""
    surveys: List[SurveyResponse]
    total: int
    skip: int
    limit: int
    has_more: bool

# ===== SCHEMAS PARA TEMPLATES =====

class SurveyTemplate(BaseModel):
    """Schema para template de encuesta"""
    name: str
    description: str
    category: str  # "docente", "coordinacion", "autoevaluacion", etc.
    template_data: SurveyCreate
    is_public: bool = True

class SurveyTemplateResponse(BaseModel):
    """Schema de respuesta para template"""
    id: str
    name: str
    description: str
    category: str
    is_public: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ===== SCHEMAS PARA ESTADÍSTICAS =====

class SurveyStats(BaseModel):
    """Schema para estadísticas de encuestas"""
    total_surveys: int
    active_surveys: int
    inactive_surveys: int
    total_questions: int
    surveys_by_type: Dict[str, int]
    recent_surveys: int

class QuestionStats(BaseModel):
    """Schema para estadísticas de preguntas"""
    question_id: str
    question_text: str
    question_type: str
    response_count: int
    average_score: Optional[float] = None
    response_distribution: Optional[Dict[str, int]] = None

# ===== SCHEMAS PARA DUPLICAR/COPIAR =====

class SurveyDuplicate(BaseModel):
    """Schema para duplicar encuesta"""
    new_title: str
    copy_questions: bool = True
    set_active: bool = False
    
    @validator('new_title')
    def validate_new_title(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('El nuevo título debe tener al menos 3 caracteres')
        return v.strip()

# ===== SCHEMAS PARA PREVIEW =====

class SurveyPreview(BaseModel):
    """Schema para preview de encuesta"""
    survey: SurveyResponse
    questions: List[QuestionResponse]
    estimated_time: int  # en minutos
    total_questions: int
    required_questions: int