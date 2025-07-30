from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    users = relationship("User", back_populates="role")

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    users = relationship("User", back_populates="department")

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    employee_code = Column(String(50), unique=True, index=True)
    phone = Column(String(20))
    
    # Relaciones con otras tablas
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    # Estados y timestamps
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    role = relationship("Role", back_populates="users")
    department = relationship("Department", back_populates="users")
    
    # Relaciones con evaluaciones
    evaluations_as_evaluator = relationship(
        "Evaluation", 
        foreign_keys="[Evaluation.evaluator_id]",
        back_populates="evaluator"
    )
    evaluations_as_evaluatee = relationship(
        "Evaluation", 
        foreign_keys="[Evaluation.evaluatee_id]",
        back_populates="evaluatee"
    )
    
    # Relaciones con asignaciones
    assignments_as_evaluator = relationship(
        "SurveyAssignment",
        foreign_keys="[SurveyAssignment.evaluator_id]",
        back_populates="evaluator"
    )
    assignments_as_evaluatee = relationship(
        "SurveyAssignment",
        foreign_keys="[SurveyAssignment.evaluatee_id]",
        back_populates="evaluatee"
    )
    assignments_created = relationship(
        "SurveyAssignment",
        foreign_keys="[SurveyAssignment.assigned_by]",
        back_populates="assigned_by_user"
    )
    
    @property
    def full_name(self) -> str:
        """Nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self) -> bool:
        """Verificar si el usuario es administrador"""
        return self.role.name == "admin"
    
    @property
    def is_coordinator(self) -> bool:
        """Verificar si el usuario es coordinador"""
        return self.role.name == "coordinador"
    
    @property
    def is_teacher(self) -> bool:
        """Verificar si el usuario es maestro"""
        return self.role.name == "maestro"
    
    def can_evaluate_user(self, other_user) -> bool:
        """
        Verificar si este usuario puede evaluar a otro usuario
        """
        # Admin puede evaluar a cualquiera
        if self.is_admin:
            return True
            
        # Coordinador puede evaluar maestros de su departamento
        if self.is_coordinator and other_user.is_teacher:
            return self.department_id == other_user.department_id
            
        # Maestros solo pueden autoevaluarse
        if self.is_teacher:
            return self.id == other_user.id
            
        return False
    
    def can_manage_department(self, department_id: int) -> bool:
        """
        Verificar si el usuario puede gestionar un departamento
        """
        # Admin puede gestionar cualquier departamento
        if self.is_admin:
            return True
            
        # Coordinador solo puede gestionar su departamento
        if self.is_coordinator:
            return self.department_id == department_id
            
        return False

    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role.name if self.role else None}')>"