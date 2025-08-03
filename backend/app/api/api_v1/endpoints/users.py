# backend/app/api/api_v1/endpoints/users.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.core.database import get_db
from app.core.security import get_password_hash
from app.api.api_v1.endpoints.auth import get_current_active_user, get_current_admin_user, get_current_coordinator_user
from app.models.user import User, Role, Department
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserList

router = APIRouter()

@router.get("/", response_model=UserList)
async def get_users(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(20, ge=1, le=100, description="Límite de registros"),
    search: Optional[str] = Query(None, description="Buscar por nombre o email"),
    role: Optional[str] = Query(None, description="Filtrar por rol"),
    department_id: Optional[int] = Query(None, description="Filtrar por departamento"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_coordinator_user)  # Coordinador+ puede ver usuarios
):
    """
    Obtener lista de usuarios con filtros, búsqueda y paginación
    """
    # Query base
    query = db.query(User).join(Role).outerjoin(Department)
    
    # Filtros por rol del usuario actual
    if not current_user.is_admin:
        # Coordinadores solo ven usuarios de su departamento
        if current_user.is_coordinator:
            query = query.filter(User.department_id == current_user.department_id)
    
    # Búsqueda por texto
    if search:
        search_filter = or_(
            User.first_name.ilike(f"%{search}%"),
            User.last_name.ilike(f"%{search}%"),
            User.email.ilike(f"%{search}%"),
            User.employee_code.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Filtro por rol
    if role:
        query = query.filter(Role.name == role)
    
    # Filtro por departamento
    if department_id:
        query = query.filter(User.department_id == department_id)
    
    # Filtro por estado activo
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    # Contar total antes de paginar
    total = query.count()
    
    # Aplicar paginación y ordenamiento
    users = query.order_by(User.first_name, User.last_name).offset(skip).limit(limit).all()
    
    return {
        "users": users,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total
    }

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener un usuario específico por ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar permisos
    if not current_user.is_admin:
        if current_user.is_coordinator:
            # Coordinador solo puede ver usuarios de su departamento
            if user.department_id != current_user.department_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para ver este usuario"
                )
        elif current_user.id != user.id:
            # Maestros solo pueden verse a sí mismos
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para ver este usuario"
            )
    
    return user

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Solo admin puede crear usuarios
):
    """
    Crear un nuevo usuario
    """
    # Verificar que el email no existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con este email"
        )
    
    # Verificar que el employee_code no existe (si se proporciona)
    if user_data.employee_code:
        existing_code = db.query(User).filter(User.employee_code == user_data.employee_code).first()
        if existing_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con este código de empleado"
            )
    
    # Verificar que el rol existe
    role = db.query(Role).filter(Role.id == user_data.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol no válido"
        )
    
    # Verificar que el departamento existe (si se proporciona)
    if user_data.department_id:
        department = db.query(Department).filter(Department.id == user_data.department_id).first()
        if not department:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Departamento no válido"
            )
    
    # Crear el usuario
    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        employee_code=user_data.employee_code,
        phone=user_data.phone,
        role_id=user_data.role_id,
        department_id=user_data.department_id,
        is_active=user_data.is_active
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualizar un usuario existente
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar permisos
    can_edit = False
    if current_user.is_admin:
        can_edit = True
    elif current_user.is_coordinator and user.department_id == current_user.department_id:
        can_edit = True
    elif current_user.id == user.id:
        # Los usuarios pueden editar algunos de sus propios datos
        can_edit = True
    
    if not can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar este usuario"
        )
    
    # Actualizar campos permitidos según rol
    update_data = user_data.dict(exclude_unset=True)
    
    # Solo admin puede cambiar rol y estado activo
    if not current_user.is_admin:
        update_data.pop("role_id", None)
        update_data.pop("is_active", None)
        # Solo admin y coordinador pueden cambiar departamento
        if not current_user.is_coordinator:
            update_data.pop("department_id", None)
    
    # Verificar email único si se está cambiando
    if "email" in update_data and update_data["email"] != user.email:
        existing_user = db.query(User).filter(
            User.email == update_data["email"],
            User.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con este email"
            )
    
    # Verificar employee_code único si se está cambiando
    if "employee_code" in update_data and update_data["employee_code"] != user.employee_code:
        existing_code = db.query(User).filter(
            User.employee_code == update_data["employee_code"],
            User.id != user_id
        ).first()
        if existing_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con este código de empleado"
            )
    
    # Hashear nueva contraseña si se proporciona
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]
    
    # Aplicar actualizaciones
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Solo admin puede eliminar
):
    """
    Eliminar un usuario (soft delete - desactivar)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # No permitir que el admin se elimine a sí mismo
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminarte a ti mismo"
        )
    
    # Soft delete - desactivar en lugar de eliminar
    user.is_active = False
    db.commit()
    
    return {"message": "Usuario desactivado exitosamente"}

@router.patch("/{user_id}/toggle-status")
async def toggle_user_status(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Activar/desactivar un usuario
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # No permitir que el admin se desactive a sí mismo
    if user.id == current_user.id and user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivarte a ti mismo"
        )
    
    user.is_active = not user.is_active
    db.commit()
    
    status_text = "activado" if user.is_active else "desactivado"
    return {"message": f"Usuario {status_text} exitosamente", "is_active": user.is_active}

@router.get("/roles/", response_model=List[dict])
async def get_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_coordinator_user)
):
    """
    Obtener lista de roles disponibles
    """
    roles = db.query(Role).all()
    return [{"id": role.id, "name": role.name, "description": role.description} for role in roles]

@router.get("/departments/", response_model=List[dict])
async def get_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener lista de departamentos disponibles
    """
    departments = db.query(Department).filter(Department.is_active == True).all()
    return [{"id": dept.id, "name": dept.name, "description": dept.description} for dept in departments]