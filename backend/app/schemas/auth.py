from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserLogin(BaseModel):
    """Schema para login de usuario"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Schema para respuesta de token JWT"""
    access_token: str
    token_type: str
    expires_in: int
    user: "UserBasic"

class UserBasic(BaseModel):
    """Schema básico de usuario para respuestas de auth"""
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    department: Optional[str] = None

class UserResponse(BaseModel):
    """Schema completo de usuario para respuesta"""
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

class ChangePassword(BaseModel):
    """Schema para cambio de password"""
    current_password: str
    new_password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "password_actual",
                "new_password": "nuevo_password_seguro"
            }
        }

class TokenData(BaseModel):
    """Schema para datos del token"""
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None