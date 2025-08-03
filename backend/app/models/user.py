from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Text, DECIMAL
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
class Survey(Base):
    __tablename__ = "surveys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    instructions = Column(Text)
    is_active = Column(Boolean, default=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    questions = relationship("Question", back_populates="survey")
    assignments = relationship("SurveyAssignment", back_populates="survey")
    evaluations = relationship("Evaluation", back_populates="survey")

class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.id"))
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default='scale')
    order_number = Column(Integer, nullable=False)
    is_required = Column(Boolean, default=True)
    min_value = Column(Integer, default=1)
    max_value = Column(Integer, default=10)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    survey = relationship("Survey", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class SurveyAssignment(Base):
    __tablename__ = "survey_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.id"))
    evaluator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    evaluatee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assignment_type = Column(String(20), nullable=False)
    status = Column(String(20), default='pending')
    due_date = Column(DateTime(timezone=True))
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # Relaciones
    survey = relationship("Survey", back_populates="assignments")
    evaluator = relationship("User", foreign_keys=[evaluator_id], back_populates="assignments_as_evaluator")
    evaluatee = relationship("User", foreign_keys=[evaluatee_id], back_populates="assignments_as_evaluatee")
    assigned_by_user = relationship("User", foreign_keys=[assigned_by], back_populates="assignments_created")
    evaluation = relationship("Evaluation", back_populates="assignment", uselist=False)

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("survey_assignments.id"))
    evaluator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    evaluatee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.id"))
    status = Column(String(20), default='in_progress')
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    total_score = Column(DECIMAL(5,2))
    comments = Column(Text)

    # Relaciones
    assignment = relationship("SurveyAssignment", back_populates="evaluation")
    evaluator = relationship("User", foreign_keys=[evaluator_id], back_populates="evaluations_as_evaluator")
    evaluatee = relationship("User", foreign_keys=[evaluatee_id], back_populates="evaluations_as_evaluatee")
    survey = relationship("Survey", back_populates="evaluations")
    answers = relationship("Answer", back_populates="evaluation")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    evaluation_id = Column(UUID(as_uuid=True), ForeignKey("evaluations.id"))
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    answer_value = Column(Integer)
    answer_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    evaluation = relationship("Evaluation", back_populates="answers")
    question = relationship("Question", back_populates="answers")