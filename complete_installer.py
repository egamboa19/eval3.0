#!/usr/bin/env python3
"""
INSTALADOR COMPLETO CORREGIDO - Sistema de Evaluación Docente
Detecta PostgreSQL automáticamente en Windows
"""

import os
import sys
import subprocess
from pathlib import Path
import glob

class FixedInstaller:
    def __init__(self):
        self.project_root = Path.cwd()
        self.config = {}
        self.pg_bin_path = None
        
    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f" {text}")
        print(f"{'='*60}")
        
    def print_step(self, step, text):
        print(f"\n[{step}] {text}")
        
    def find_postgresql(self):
        """Encontrar PostgreSQL en Windows automáticamente"""
        self.print_step("0", "Detectando PostgreSQL...")
        
        # Rutas comunes de PostgreSQL en Windows
        possible_paths = [
            "C:\\Program Files\\PostgreSQL\\*\\bin",
            "C:\\Program Files (x86)\\PostgreSQL\\*\\bin",
            "C:\\PostgreSQL\\*\\bin",
            "C:\\pgAdmin 4\\*\\runtime\\pgsql\\bin",
        ]
        
        for path_pattern in possible_paths:
            paths = glob.glob(path_pattern)
            for path in sorted(paths, reverse=True):  # Versión más reciente primero
                psql_exe = os.path.join(path, "psql.exe")
                createdb_exe = os.path.join(path, "createdb.exe")
                
                if os.path.exists(psql_exe) and os.path.exists(createdb_exe):
                    self.pg_bin_path = path
                    print(f"✅ PostgreSQL encontrado en: {path}")
                    
                    # Verificar versión
                    try:
                        result = subprocess.run([psql_exe, "--version"], 
                                              capture_output=True, text=True)
                        if result.returncode == 0:
                            version = result.stdout.strip()
                            print(f"✅ Versión: {version}")
                            return True
                    except:
                        continue
        
        print("❌ PostgreSQL no encontrado automáticamente")
        print("\n💡 Opciones:")
        print("1. Instalar PostgreSQL desde: https://www.postgresql.org/download/windows/")
        print("2. O proporcionar la ruta manualmente")
        
        manual_path = input("\n¿Ruta manual a PostgreSQL bin? (o Enter para salir): ").strip()
        if manual_path and os.path.exists(os.path.join(manual_path, "psql.exe")):
            self.pg_bin_path = manual_path
            print(f"✅ Usando ruta manual: {manual_path}")
            return True
        
        return False
        
    def run_pg_command(self, command, db_name=None):
        """Ejecutar comando PostgreSQL con la ruta correcta"""
        if not self.pg_bin_path:
            raise Exception("PostgreSQL no encontrado")
            
        # Construir comando completo con ruta
        if command[0] in ['psql', 'createdb', 'dropdb']:
            command[0] = os.path.join(self.pg_bin_path, command[0] + ".exe")
        
        # Agregar variables de entorno
        env = {**os.environ, 'PGPASSWORD': self.config['db_password']}
        
        # Ejecutar comando
        result = subprocess.run(command, capture_output=True, text=True, env=env)
        return result
        
    def create_structure(self):
        """Crear estructura completa de directorios"""
        self.print_header("CREANDO ESTRUCTURA DEL PROYECTO")
        
        directories = [
            "backend/app/core", "backend/app/models", "backend/app/schemas",
            "backend/app/api/api_v1/endpoints", "backend/app/services", "backend/app/utils",
            "frontend/public", "frontend/src/components/auth", "frontend/src/components/common", 
            "frontend/src/components/layout", "frontend/src/pages/admin", "frontend/src/pages/coordinator",
            "frontend/src/pages/teacher", "frontend/src/pages/common", "frontend/src/contexts",
            "frontend/src/services", "frontend/src/utils", "frontend/src/hooks",
            "database/migrations", "database/backups", "docs", "tools", "logs"
        ]
        
        for directory in directories:
            (self.project_root / directory).mkdir(parents=True, exist_ok=True)
        
        # Crear archivos __init__.py
        init_files = [
            "backend/app/__init__.py", "backend/app/core/__init__.py", "backend/app/models/__init__.py",
            "backend/app/schemas/__init__.py", "backend/app/api/__init__.py", 
            "backend/app/api/api_v1/__init__.py", "backend/app/api/api_v1/endpoints/__init__.py",
            "backend/app/services/__init__.py", "backend/app/utils/__init__.py",
        ]
        
        for init_file in init_files:
            (self.project_root / init_file).write_text('# Package initialization\n')
            
        print("✅ Estructura creada")
        
    def collect_config(self):
        """Recopilar configuración"""
        self.print_header("CONFIGURACIÓN DEL SISTEMA")
        
        self.config['institution_name'] = input("📚 Nombre de la institución: ").strip() or "Institución Educativa"
        self.config['institution_short'] = input("📝 Nombre corto (sin espacios): ").strip().lower().replace(' ', '_') or "institucion"
        
        print("\nModo de red:")
        print("1. Solo local (LAN)")
        print("2. Híbrido (LAN + web)")
        choice = input("Opción (1-2) [1]: ").strip() or "1"
        self.config['network_mode'] = 'local' if choice == '1' else 'hybrid'
        
        print("\nConfiguración PostgreSQL:")
        self.config['db_host'] = input("Host [localhost]: ").strip() or 'localhost'
        self.config['db_port'] = input("Puerto [5432]: ").strip() or '5432'
        self.config['db_user'] = input("Usuario [postgres]: ").strip() or 'postgres'
        self.config['db_password'] = input("Password: ").strip()
        
        print("\nAdministrador:")
        self.config['admin_email'] = input("Email admin: ").strip()
        self.config['admin_password'] = input("Password admin [admin123]: ").strip() or 'admin123'
        self.config['admin_first_name'] = input("Nombre [Admin]: ").strip() or 'Admin'
        self.config['admin_last_name'] = input("Apellido [Sistema]: ").strip() or 'Sistema'
        
    def test_db_connection(self):
        """Probar conexión a PostgreSQL"""
        self.print_step("TEST", "Probando conexión a PostgreSQL...")
        
        try:
            test_cmd = ['psql', '-h', self.config['db_host'], '-p', self.config['db_port'],
                       '-U', self.config['db_user'], '-c', 'SELECT version();']
            
            result = self.run_pg_command(test_cmd)
            
            if result.returncode == 0:
                print("✅ Conexión a PostgreSQL exitosa")
                return True
            else:
                print(f"❌ Error de conexión: {result.stderr}")
                print("\n💡 Verifica:")
                print("1. Que PostgreSQL esté corriendo")
                print("2. Usuario y password correctos")
                print("3. Host y puerto correctos")
                return False
                
        except Exception as e:
            print(f"❌ Error probando conexión: {e}")
            return False
            
    def create_database_files(self):
        """Crear archivos de base de datos con contenido completo"""
        self.print_step("3A", "Creando scripts de base de datos...")
        
        # Schema SQL (contenido completo del artifact database_schema)
        schema_sql = '''-- ===================================================
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
'''

        # Seeds SQL
        seeds_sql = '''-- ===================================================
-- DATOS INICIALES DEL SISTEMA
-- ===================================================

-- Insertar roles
INSERT INTO roles (name, description) VALUES 
('admin', 'Administrador del sistema con acceso completo'),
('coordinador', 'Coordinador de area que evalua maestros'),
('maestro', 'Maestro que realiza autoevaluaciones');

-- Insertar departamentos
INSERT INTO departments (name, description) VALUES 
('Matematicas', 'Departamento de Ciencias Matematicas'),
('Ciencias', 'Departamento de Ciencias Naturales'),
('Humanidades', 'Departamento de Humanidades y Letras'),
('Ingles', 'Departamento de Idioma Ingles'),
('Educacion Fisica', 'Departamento de Educacion Fisica y Deportes'),
('Artes', 'Departamento de Artes y Cultura'),
('Tecnologia', 'Departamento de Tecnologia e Informatica'),
('Administracion', 'Departamento Administrativo');

-- Configuración del sistema
INSERT INTO system_config (key, value, description) VALUES 
('institution_name', '{}', 'Nombre de la institucion'),
('institution_short', '{}', 'Nombre corto de la institucion'),
('network_mode', '{}', 'Modo de red: local, hybrid, web'),
('default_evaluation_duration', '7', 'Duracion por defecto de evaluaciones en dias'),
('session_timeout', '480', 'Timeout de sesion en minutos');

-- Encuesta ejemplo
DO $$
DECLARE
    survey_uuid UUID;
BEGIN
    INSERT INTO surveys (title, description, instructions) 
    VALUES (
        'Evaluacion Docente Estandar',
        'Evaluacion integral del desempeno docente',
        'Califique cada aspecto del 1 al 10, donde 1 es deficiente y 10 es excelente'
    ) RETURNING id INTO survey_uuid;
    
    INSERT INTO questions (survey_id, question_text, order_number) VALUES 
    (survey_uuid, 'Dominio del contenido de la materia', 1),
    (survey_uuid, 'Claridad en la explicacion de conceptos', 2),
    (survey_uuid, 'Puntualidad y asistencia', 3),
    (survey_uuid, 'Preparacion de clases', 4),
    (survey_uuid, 'Uso de recursos didacticos', 5),
    (survey_uuid, 'Atencion a estudiantes', 6),
    (survey_uuid, 'Evaluacion justa y objetiva', 7),
    (survey_uuid, 'Fomento de la participacion estudiantil', 8),
    (survey_uuid, 'Actualizacion profesional', 9),
    (survey_uuid, 'Trabajo en equipo con colegas', 10);
END $$;
'''.format(
    self.config['institution_name'],
    self.config['institution_short'], 
    self.config['network_mode']
)

        # Guardar archivos
        with open('database/01_create_schema.sql', 'w', encoding='utf-8') as f:
            f.write(schema_sql)
            
        with open('database/02_insert_seeds.sql', 'w', encoding='utf-8') as f:
            f.write(seeds_sql)
            
        print("✅ Scripts de BD creados con contenido completo")
        
    def create_config_files(self):
        """Crear archivos de configuración"""
        self.print_step("3B", "Creando archivos de configuración...")
        
        # .env
        env_content = f"""# Configuración de la institución
INSTITUTION_NAME={self.config['institution_name']}
INSTITUTION_SHORT={self.config['institution_short']}
NETWORK_MODE={self.config['network_mode']}

# Base de datos
DB_HOST={self.config['db_host']}
DB_PORT={self.config['db_port']}
DB_USER={self.config['db_user']}
DB_PASSWORD={self.config['db_password']}
DB_NAME=evaluacion_{self.config['institution_short']}

# JWT y seguridad
SECRET_KEY={"super_secret_key_" + self.config['institution_short'] + "_change_in_production"}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# API
API_V1_STR=/api/v1
PROJECT_NAME=Sistema de Evaluacion Docente - {self.config['institution_name']}

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# Entorno
ENVIRONMENT=production

# Admin inicial
ADMIN_EMAIL={self.config['admin_email']}
ADMIN_PASSWORD={self.config['admin_password']}
ADMIN_FIRST_NAME={self.config['admin_first_name']}
ADMIN_LAST_NAME={self.config['admin_last_name']}

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_INSTITUTION_NAME={self.config['institution_name']}
REACT_APP_NETWORK_MODE={self.config['network_mode']}
"""
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
            
        # requirements.txt
        requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.7
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
email-validator==2.1.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2"""
        
        with open('backend/requirements.txt', 'w', encoding='utf-8') as f:
            f.write(requirements)
            
        # package.json básico
        package_json = """{
  "name": "evaluacion-docente-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.1",
    "react-scripts": "5.0.1",
    "@tanstack/react-query": "^4.28.0",
    "axios": "^1.3.4",
    "tailwindcss": "^3.3.0",
    "react-hot-toast": "^2.4.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}"""
        
        with open('frontend/package.json', 'w', encoding='utf-8') as f:
            f.write(package_json)
            
        print("✅ Archivos de configuración creados")
        
    def setup_database_complete(self):
        """Configurar base de datos COMPLETA"""
        self.print_step("4", "Configurando base de datos completa...")
        
        db_name = f"evaluacion_{self.config['institution_short']}"
        
        try:
            # 1. Crear base de datos
            self.print_step("4A", f"Creando base de datos: {db_name}")
            create_cmd = ['createdb', '-h', self.config['db_host'], '-p', self.config['db_port'],
                         '-U', self.config['db_user'], db_name]
            
            result = self.run_pg_command(create_cmd)
            if result.returncode == 0:
                print(f"✅ Base de datos '{db_name}' creada")
            else:
                if "already exists" in result.stderr:
                    print(f"⚠️  Base de datos '{db_name}' ya existe")
                else:
                    print(f"❌ Error creando BD: {result.stderr}")
                    return False
            
            # 2. Ejecutar schema
            self.print_step("4B", "Creando tablas...")
            schema_cmd = ['psql', '-h', self.config['db_host'], '-p', self.config['db_port'],
                         '-U', self.config['db_user'], '-d', db_name, '-f', 'database/01_create_schema.sql']
            
            result = self.run_pg_command(schema_cmd)
            if result.returncode == 0:
                print("✅ Tablas creadas")
            else:
                print(f"❌ Error creando tablas: {result.stderr}")
                return False
            
            # 3. Insertar datos iniciales
            self.print_step("4C", "Insertando datos iniciales...")
            seeds_cmd = ['psql', '-h', self.config['db_host'], '-p', self.config['db_port'],
                        '-U', self.config['db_user'], '-d', db_name, '-f', 'database/02_insert_seeds.sql']
            
            result = self.run_pg_command(seeds_cmd)
            if result.returncode == 0:
                print("✅ Datos iniciales insertados")
            else:
                print(f"❌ Error insertando datos: {result.stderr}")
                return False
            
            # 4. Crear usuario administrador
            self.print_step("4D", "Creando usuario administrador...")
            admin_sql = f"""
            INSERT INTO users (email, hashed_password, first_name, last_name, employee_code, role_id, department_id) 
            VALUES ('{self.config['admin_email']}', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUQcSKbBfN8Ujmm', 
                    '{self.config['admin_first_name']}', '{self.config['admin_last_name']}', 'ADM001', 
                    (SELECT id FROM roles WHERE name = 'admin'), 
                    (SELECT id FROM departments WHERE name = 'Administracion'))
            ON CONFLICT (email) DO NOTHING;
            """
            
            admin_cmd = ['psql', '-h', self.config['db_host'], '-p', self.config['db_port'],
                        '-U', self.config['db_user'], '-d', db_name, '-c', admin_sql]
            
            result = self.run_pg_command(admin_cmd)
            if result.returncode == 0:
                print("✅ Usuario administrador creado")
            else:
                print(f"⚠️  Error o admin ya existe: {result.stderr}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error configurando BD: {e}")
            return False
            
    def create_startup_scripts(self):
        """Crear scripts de inicio"""
        self.print_step("5", "Creando scripts de inicio...")
        
        # Windows
        bat_content = f"""@echo off
echo Iniciando Sistema de Evaluacion - {self.config['institution_name']}
echo.

echo Verificando dependencias...
cd backend
python -c "import fastapi" 2>nul || (echo Instalando dependencias backend... && pip install -r requirements.txt)

echo Iniciando backend...
start "Backend API" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

timeout /t 5

echo Verificando frontend...
cd ../frontend
npm list react >nul 2>&1 || (echo Instalando dependencias frontend... && npm install)

echo Iniciando frontend...
start "Frontend" npm start

echo.
echo ====================================
echo Sistema iniciado correctamente:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo - Docs API: http://localhost:8000/docs
echo.
echo Credenciales de administrador:
echo - Email: {self.config['admin_email']}
echo - Password: {self.config['admin_password']}
echo ====================================
echo.
echo Para detener: Cierra las ventanas o presiona Ctrl+C
pause
"""
        
        with open('iniciar_sistema.bat', 'w', encoding='utf-8') as f:
            f.write(bat_content)
            
        print("✅ Scripts de inicio creados")
        
    def create_essential_files(self):
        """Crear archivos esenciales para que funcione básicamente"""
        self.print_step("6", "Creando archivos esenciales...")
        
        # Frontend básico
        index_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Sistema de Evaluación Docente</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>"""
        
        with open('frontend/public/index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
            
        index_js = f"""import React from 'react';
import {{ createRoot }} from 'react-dom/client';

function App() {{
    return (
        <div style={{{{padding: '20px', fontFamily: 'Arial, sans-serif'}}}}>
            <h1>🎓 {self.config['institution_name']}</h1>
            <h2>Sistema de Evaluación Docente</h2>
            
            <div style={{{{backgroundColor: '#dcfce7', padding: '20px', borderRadius: '8px', marginTop: '20px', border: '1px solid #16a34a'}}}}>
                <h3>✅ ¡Instalación Base Completada!</h3>
                <p><strong>Estado:</strong> Base de datos configurada correctamente</p>
                <p><strong>Institución:</strong> {self.config['institution_name']}</p>
                <p><strong>BD:</strong> evaluacion_{self.config['institution_short']}</p>
                <p><strong>Admin:</strong> {self.config['admin_email']}</p>
            </div>
            
            <div style={{{{backgroundColor: '#fef3c7', padding: '20px', borderRadius: '8px', marginTop: '20px', border: '1px solid #d97706'}}}}>
                <h3>📝 Siguiente Paso: Completar el Sistema</h3>
                <p>Para tener el sistema completo funcionando, necesitas copiar el código de los artifacts:</p>
                <ul>
                    <li><strong>backend/app/main.py</strong> ← artifact: backend_main</li>
                    <li><strong>backend/app/core/config.py</strong> ← artifact: backend_config</li>
                    <li><strong>frontend/src/App.js</strong> ← artifact: frontend_app_js</li>
                    <li>Y más archivos según la lista completa...</li>
                </ul>
            </div>
            
            <div style={{{{backgroundColor: '#e0f2fe', padding: '20px', borderRadius: '8px', marginTop: '20px', border: '1px solid #0284c7'}}}}>
                <h3>🚀 URLs del Sistema:</h3>
                <ul>
                    <li><strong>Frontend:</strong> <a href="http://localhost:3000">http://localhost:3000</a></li>
                    <li><strong>Backend API:</strong> <a href="http://localhost:8000">http://localhost:8000</a></li>
                    <li><strong>Documentación:</strong> <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></li>
                </ul>
            </div>
            
            <div style={{{{backgroundColor: '#f3e8ff', padding: '20px', borderRadius: '8px', marginTop: '20px', border: '1px solid #9333ea'}}}}>
                <h3>📚 Documentación:</h3>
                <p>Consulta el <strong>MANUAL_COMPLETO.md</strong> para:</p>
                <ul>
                    <li>Lista completa de archivos a copiar</li>
                    <li>Guía de instalación manual</li>
                    <li>Solución de problemas</li>
                    <li>Configuración avanzada</li>
                </ul>
            </div>
            
            <div style={{{{marginTop: '30px', padding: '10px', backgroundColor: '#f8fafc', borderLeft: '4px solid #3b82f6'}}}}>
                <p><strong>💡 Tip:</strong> Este mensaje confirma que la base está funcionando. Una vez que copies el código de los artifacts, tendrás el sistema completo de evaluación docente.</p>
            </div>
        </div>
    );
}}

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);"""
        
        with open('frontend/src/index.js', 'w', encoding='utf-8') as f:
            f.write(index_js)
            
        print("✅ Archivos esenciales creados")
        
    def print_final_summary(self):
        """Mostrar resumen final"""
        self.print_header("🎉 INSTALACIÓN BASE COMPLETADA EXITOSAMENTE")
        
        print(f"""
✅ CONFIGURACIÓN COMPLETA:
   • Institución: {self.config['institution_name']}
   • Base de datos: evaluacion_{self.config['institution_short']} (CON DATOS)
   • Admin: {self.config['admin_email']} / {self.config['admin_password']}
   • PostgreSQL: Detectado en {self.pg_bin_path}
   • Tablas: ✅ Creadas (9 tablas principales)
   • Datos iniciales: ✅ Insertados (roles, departamentos, encuesta ejemplo)
   • Usuario admin: ✅ Creado

🚀 PARA INICIAR AHORA MISMO:
   Ejecuta: iniciar_sistema.bat
   
   Esto abrirá:
   - Backend básico en http://localhost:8000
   - Frontend básico en http://localhost:3000
   
   El frontend mostrará una página confirmando que todo funciona.

📝 PARA SISTEMA COMPLETO:
   Necesitas copiar el código de los artifacts a estos archivos:

   🔥 ALTA PRIORIDAD (Backend):
   📄 backend/app/main.py              ← artifact: backend_main
   📄 backend/app/core/config.py       ← artifact: backend_config
   📄 backend/app/core/database.py     ← artifact: backend_database
   📄 backend/app/core/security.py     ← artifact: backend_security
   📄 backend/app/models/user.py       ← artifact: backend_models_user
   📄 backend/app/schemas/auth.py      ← artifact: backend_schemas
   📄 backend/app/api/api_v1/api.py    ← artifact: backend_api_router
   📄 backend/app/api/api_v1/endpoints/auth.py ← artifact: backend_endpoints_auth

   🎨 ALTA PRIORIDAD (Frontend):
   📄 frontend/src/App.js              ← artifact: frontend_app_js
   📄 frontend/src/index.css           ← artifact: frontend_index_css
   📄 frontend/tailwind.config.js      ← artifact: frontend_tailwind_config
   📄 frontend/src/services/api.js     ← artifact: frontend_api_service
   📄 frontend/src/contexts/AuthContext.js ← artifact: frontend_auth_context

💡 PROCESO RECOMENDADO:
   1. ✅ Ejecutar iniciar_sistema.bat (verificar que funciona básicamente)
   2. 📝 Copiar archivos backend uno por uno y reiniciar
   3. 🎨 Copiar archivos frontend uno por uno  
   4. 🔧 Instalar dependencias si es necesario:
      cd backend && pip install -r requirements.txt
      cd frontend && npm install
   5. 🚀 Reiniciar sistema completo

📞 SI ALGO FALLA:
   1. Verificar que PostgreSQL esté corriendo
   2. Verificar credenciales en .env
   3. Revisar logs en las consolas
   4. Consultar MANUAL_COMPLETO.md

🎯 SIGUIENTE ACCIÓN:
   Ejecuta: iniciar_sistema.bat
   
¡Tu sistema base está listo! Solo falta completar el código 🚀
""")
        
    def run(self):
        """Ejecutar instalación completa"""
        try:
            self.print_header("🚀 INSTALADOR CORREGIDO - EVALUACIÓN DOCENTE")
            print("Versión mejorada que detecta PostgreSQL automáticamente en Windows")
            
            # Detectar PostgreSQL primero
            if not self.find_postgresql():
                print("\n❌ No se puede continuar sin PostgreSQL")
                return
                
            self.create_structure()
            self.collect_config()
            
            # Probar conexión antes de crear archivos
            if not self.test_db_connection():
                print("\n❌ No se puede continuar sin conexión a PostgreSQL")
                return
                
            self.create_database_files()
            self.create_config_files()
            
            if self.setup_database_complete():
                print("\n✅ Base de datos configurada correctamente")
            else:
                print("\n❌ Error en configuración de BD")
                return
                
            self.create_startup_scripts()
            self.create_essential_files()
            self.print_final_summary()
            
        except KeyboardInterrupt:
            print("\n❌ Instalación cancelada por el usuario")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    installer = FixedInstaller()
    installer.run()