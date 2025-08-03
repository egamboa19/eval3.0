# backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    """Schema base de usuario"""
    email: EmailStr
    first_name: str
    last_name: str
    employee_code: Optional[str] = None
    phone: Optional[str] = None
    role_id: int
    department_id: Optional[int] = None
    is_active: bool = True

class UserCreate(UserBase):
    """Schema para crear usuario"""
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Nombre y apellido deben tener al menos 2 caracteres')
        return v.strip().title()
    
    @validator('employee_code')
    def validate_employee_code(cls, v):
        if v and len(v.strip()) < 3:
            raise ValueError('Código de empleado debe tener al menos 3 caracteres')
        return v.strip().upper() if v else None

class UserUpdate(BaseModel):
    """Schema para actualizar usuario"""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    employee_code: Optional[str] = None
    phone: Optional[str] = None
    role_id: Optional[int] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if v and len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if v and len(v.strip()) < 2:
            raise ValueError('Nombre y apellido deben tener al menos 2 caracteres')
        return v.strip().title() if v else None
    
    @validator('employee_code')
    def validate_employee_code(cls, v):
        if v and len(v.strip()) < 3:
            raise ValueError('Código de empleado debe tener al menos 3 caracteres')
        return v.strip().upper() if v else None

class UserResponse(BaseModel):
    """Schema para respuesta de usuario"""
    id: str
    email: str
    first_name: str
    last_name: str
    employee_code: Optional[str] = None
    phone: Optional[str] = None
    role: str
    department: Optional[str] = None
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        
    @validator('id', pre=True)
    def convert_uuid_to_string(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v
    
    @validator('role', pre=True)
    def extract_role_name(cls, v):
        if hasattr(v, 'name'):
            return v.name
        return v
    
    @validator('department', pre=True)
    def extract_department_name(cls, v):
        if v and hasattr(v, 'name'):
            return v.name
        return v

class UserSummary(BaseModel):
    """Schema resumido de usuario para listas"""
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    department: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True
        
    @validator('id', pre=True)
    def convert_uuid_to_string(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v
    
    @validator('role', pre=True)
    def extract_role_name(cls, v):
        if hasattr(v, 'name'):
            return v.name
        return v
    
    @validator('department', pre=True)
    def extract_department_name(cls, v):
        if v and hasattr(v, 'name'):
            return v.name
        return v

class UserList(BaseModel):
    """Schema para lista paginada de usuarios"""
    users: List[UserResponse]
    total: int
    skip: int
    limit: int
    has_more: bool

class RoleSchema(BaseModel):
    """Schema de rol"""
    id: int
    name: str
    description: Optional[str] = None

class DepartmentSchema(BaseModel):
    """Schema de departamento"""
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool

class UserStats(BaseModel):
    """Schema para estadísticas de usuarios"""
    total_users: int
    active_users: int
    inactive_users: int
    users_by_role: dict
    users_by_department: dict
    recent_registrations: int