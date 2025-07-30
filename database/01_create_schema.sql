-- ===================================================
-- SCRIPT DE CREACION DE BASE DE DATOS
-- Sistema de Evaluacion Docente - Local/Hibrido  
-- ===================================================

-- Crear extension para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ===================================================
-- TABLA: roles
-- ===================================================
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
-- TABLA: departments
-- ===================================================
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
-- TABLA: users
-- ===================================================
CREATE TABLE users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    employee_code VARCHAR(50) UNIQUE,
    phone VARCHAR(20),
    role_id INTEGER REFERENCES roles(id) NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
-- TABLA: surveys
-- ===================================================
CREATE TABLE surveys (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    instructions TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
-- TABLA: questions
-- ===================================================
CREATE TABLE questions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    survey_id UUID REFERENCES surveys(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) DEFAULT 'scale',
    order_number INTEGER NOT NULL,
    is_required BOOLEAN DEFAULT TRUE,
    min_value INTEGER DEFAULT 1,
    max_value INTEGER DEFAULT 10,
    options JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
-- TABLA: survey_assignments
-- ===================================================
CREATE TABLE survey_assignments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    survey_id UUID REFERENCES surveys(id) ON DELETE CASCADE,
    evaluator_id UUID REFERENCES users(id),
    evaluatee_id UUID REFERENCES users(id),
    assignment_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    due_date TIMESTAMP,
    assigned_by UUID REFERENCES users(id),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- ===================================================
-- TABLA: evaluations
-- ===================================================
CREATE TABLE evaluations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    assignment_id UUID REFERENCES survey_assignments(id) ON DELETE CASCADE,
    evaluator_id UUID REFERENCES users(id),
    evaluatee_id UUID REFERENCES users(id),
    survey_id UUID REFERENCES surveys(id),
    status VARCHAR(20) DEFAULT 'in_progress',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    total_score DECIMAL(5,2),
    comments TEXT
);

-- ===================================================
-- TABLA: answers
-- ===================================================
CREATE TABLE answers (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    evaluation_id UUID REFERENCES evaluations(id) ON DELETE CASCADE,
    question_id UUID REFERENCES questions(id),
    answer_value INTEGER,
    answer_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
-- TABLA: evaluation_comparisons
-- ===================================================
CREATE TABLE evaluation_comparisons (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    evaluatee_id UUID REFERENCES users(id),
    survey_id UUID REFERENCES surveys(id),
    self_evaluation_id UUID REFERENCES evaluations(id),
    coordinator_evaluation_id UUID REFERENCES evaluations(id),
    comparison_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    average_difference DECIMAL(5,2),
    status VARCHAR(20) DEFAULT 'pending'
);

-- ===================================================
-- TABLA: system_config
-- ===================================================
CREATE TABLE system_config (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
-- INDICES
-- ===================================================
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role_id);
CREATE INDEX idx_users_department ON users(department_id);
CREATE INDEX idx_users_active ON users(is_active);

CREATE INDEX idx_questions_survey ON questions(survey_id);
CREATE INDEX idx_assignments_evaluator ON survey_assignments(evaluator_id);
CREATE INDEX idx_assignments_evaluatee ON survey_assignments(evaluatee_id);
CREATE INDEX idx_evaluations_evaluator ON evaluations(evaluator_id);
CREATE INDEX idx_evaluations_evaluatee ON evaluations(evaluatee_id);

-- ===================================================
-- TRIGGERS
-- ===================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_surveys_updated_at BEFORE UPDATE ON surveys FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
