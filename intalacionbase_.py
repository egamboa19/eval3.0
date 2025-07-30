#!/usr/bin/env python3
"""
INSTALADOR RÁPIDO - Sistema de Evaluación Docente
Crea estructura + configuración + base de datos
El código se copia manualmente de los artifacts
"""

import os
import sys
import subprocess
from pathlib import Path

class QuickInstaller:
    def __init__(self):
        self.project_root = Path.cwd()
        self.config = {}
        
    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f" {text}")
        print(f"{'='*60}")
        
    def print_step(self, step, text):
        print(f"\n[{step}] {text}")
        
    def create_structure(self):
        """Crear estructura completa de directorios"""
        self.print_header("CREANDO ESTRUCTURA DEL PROYECTO")
        
        directories = [
            # Backend
            "backend/app/core",
            "backend/app/models", 
            "backend/app/schemas",
            "backend/app/api/api_v1/endpoints",
            "backend/app/services",
            "backend/app/utils",
            
            # Frontend
            "frontend/public",
            "frontend/src/components/auth",
            "frontend/src/components/common", 
            "frontend/src/components/layout",
            "frontend/src/pages/admin",
            "frontend/src/pages/coordinator",
            "frontend/src/pages/teacher",
            "frontend/src/pages/common",
            "frontend/src/contexts",
            "frontend/src/services",
            "frontend/src/utils",
            "frontend/src/hooks",
            
            # Database y otros
            "database/migrations",
            "database/backups",
            "docs", "tools", "logs"
        ]
        
        print("Creando directorios...")
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {directory}")
        
        # Crear archivos __init__.py
        init_files = [
            "backend/app/__init__.py",
            "backend/app/core/__init__.py",
            "backend/app/models/__init__.py",
            "backend/app/schemas/__init__.py", 
            "backend/app/api/__init__.py",
            "backend/app/api/api_v1/__init__.py",
            "backend/app/api/api_v1/endpoints/__init__.py",
            "backend/app/services/__init__.py",
            "backend/app/utils/__init__.py",
        ]
        
        for init_file in init_files:
            file_path = self.project_root / init_file
            file_path.write_text('# Package initialization\n')
            
        print("✅ Estructura creada")
        
    def collect_config(self):
        """Recopilar configuración básica"""
        self.print_header("CONFIGURACIÓN BÁSICA")
        
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
        
    def create_config_files(self):
        """Crear archivos de configuración"""
        self.print_step("3", "Creando archivos de configuración...")
        
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
        
        with open('.env', 'w') as f:
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
        
        with open('backend/requirements.txt', 'w') as f:
            f.write(requirements)
            
        # package.json
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
    "zustand": "^4.3.6",
    "react-hook-form": "^7.43.5",
    "axios": "^1.3.4",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.21",
    "chart.js": "^4.2.1",
    "react-chartjs-2": "^5.2.0",
    "framer-motion": "^10.8.0",
    "lucide-react": "^0.216.0",
    "react-hot-toast": "^2.4.0",
    "date-fns": "^2.29.3"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  }
}"""
        
        with open('frontend/package.json', 'w') as f:
            f.write(package_json)
            
        print("✅ Archivos de configuración creados")
        
    def setup_database(self):
        """Configurar base de datos"""
        self.print_step("4", "Configurando base de datos...")
        
        db_name = f"evaluacion_{self.config['institution_short']}"
        
        try:
            # Verificar conexión
            env = {**os.environ, 'PGPASSWORD': self.config['db_password']}
            
            # Crear BD
            create_cmd = ['createdb', '-h', self.config['db_host'], '-p', self.config['db_port'],
                         '-U', self.config['db_user'], db_name]
            
            result = subprocess.run(create_cmd, capture_output=True, text=True, env=env)
            
            if result.returncode == 0:
                print(f"✅ Base de datos '{db_name}' creada")
                return True
            else:
                print(f"⚠️  Error o BD ya existe: {result.stderr}")
                return True  # Continuar aunque ya exista
                
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

echo Iniciando backend...
cd backend
start "Backend API" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

timeout /t 3

echo Iniciando frontend...
cd ../frontend
start "Frontend" npm start

echo.
echo Sistema iniciado:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo - Admin: {self.config['admin_email']} / {self.config['admin_password']}
pause
"""
        
        with open('iniciar_sistema.bat', 'w') as f:
            f.write(bat_content)
            
        # Linux/Mac
        sh_content = f"""#!/bin/bash
echo "Iniciando Sistema de Evaluacion - {self.config['institution_name']}"
echo

echo "Iniciando backend..."
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

sleep 3

echo "Iniciando frontend..."
cd ../frontend  
npm start &
FRONTEND_PID=$!

echo
echo "Sistema iniciado:"
echo "- Backend: http://localhost:8000"
echo "- Frontend: http://localhost:3000"
echo "- Admin: {self.config['admin_email']} / {self.config['admin_password']}"
echo

echo "Presiona Ctrl+C para detener"
wait
"""
        
        with open('iniciar_sistema.sh', 'w') as f:
            f.write(sh_content)
            
        os.chmod('iniciar_sistema.sh', 0o755)
        print("✅ Scripts de inicio creados")
        
    def create_file_map(self):
        """Crear mapeo de archivos para copiar manualmente"""
        file_map = {
            # Backend
            "backend/app/main.py": "Copiar artifact: backend_main",
            "backend/app/core/config.py": "Copiar artifact: backend_config", 
            "backend/app/core/database.py": "Copiar artifact: backend_database",
            "backend/app/core/security.py": "Copiar artifact: backend_security",
            "backend/app/models/user.py": "Copiar artifact: backend_models_user",
            "backend/app/schemas/auth.py": "Copiar artifact: backend_schemas",
            "backend/app/api/api_v1/api.py": "Copiar artifact: backend_api_router",
            "backend/app/api/api_v1/endpoints/auth.py": "Copiar artifact: backend_endpoints_auth",
            
            # Frontend
            "frontend/src/App.js": "Copiar artifact: frontend_app_js",
            "frontend/src/index.js": "Crear manualmente (simple)",
            "frontend/src/index.css": "Copiar artifact: frontend_index_css",
            "frontend/tailwind.config.js": "Copiar artifact: frontend_tailwind_config",
            "frontend/src/services/api.js": "Copiar artifact: frontend_api_service",
            "frontend/src/contexts/AuthContext.js": "Copiar artifact: frontend_auth_context",
            "frontend/src/contexts/ThemeContext.js": "Copiar artifact: frontend_theme_context",
            "frontend/src/components/auth/ProtectedRoute.js": "Copiar artifact: frontend_protected_route",
            "frontend/src/components/common/LoadingSpinner.js": "Copiar artifact: frontend_loading_spinner",
            
            # Database
            "database/01_create_schema.sql": "Copiar artifact: database_schema",
            "database/02_insert_seeds.sql": "Copiar artifact: database_seeds",
        }
        
        print("\n📋 ARCHIVOS A CREAR MANUALMENTE:")
        print("="*50)
        
        for file_path, instruction in file_map.items():
            print(f"📄 {file_path}")
            print(f"   → {instruction}")
            print()
            
        return file_map
        
    def print_next_steps(self):
        """Mostrar próximos pasos"""
        self.print_header("🎉 INSTALACIÓN BASE COMPLETADA")
        
        print(f"""
📋 CONFIGURACIÓN CREADA:
   • Institución: {self.config['institution_name']}
   • Base de datos: evaluacion_{self.config['institution_short']}
   • Admin: {self.config['admin_email']}

📝 PRÓXIMOS PASOS:

1. COPIAR CÓDIGO DE ARTIFACTS:
   - Usa la lista de archivos mostrada arriba
   - Copia el contenido de cada artifact a su archivo correspondiente
   - Los artifacts están en la conversación anterior

2. EJECUTAR SCRIPTS DE BD:
   ```
   psql -U postgres -d evaluacion_{self.config['institution_short']} -f database/01_create_schema.sql
   psql -U postgres -d evaluacion_{self.config['institution_short']} -f database/02_insert_seeds.sql
   ```

3. INSTALAR DEPENDENCIAS:
   ```
   cd backend && pip install -r requirements.txt
   cd ../frontend && npm install
   ```

4. CREAR USUARIO ADMIN:
   ```
   psql -U postgres -d evaluacion_{self.config['institution_short']} -c "
   INSERT INTO users (email, hashed_password, first_name, last_name, employee_code, role_id, department_id) 
   VALUES ('{self.config['admin_email']}', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUQcSKbBfN8Ujmm', 
           '{self.config['admin_first_name']}', '{self.config['admin_last_name']}', 'ADM001', 
           (SELECT id FROM roles WHERE name = 'admin'), 
           (SELECT id FROM departments WHERE name = 'Administracion'));"
   ```

5. INICIAR SISTEMA:
   Windows: iniciar_sistema.bat
   Linux/Mac: ./iniciar_sistema.sh

💡 TIP: Puedes crear los archivos uno por uno y probar gradualmente
""")
        
    def run(self):
        """Ejecutar instalación rápida"""
        try:
            self.print_header("🚀 INSTALADOR RÁPIDO - EVALUACIÓN DOCENTE")
            
            self.create_structure()
            self.collect_config()
            self.create_config_files()
            self.setup_database()
            self.create_startup_scripts()
            self.create_file_map()
            self.print_next_steps()
            
        except KeyboardInterrupt:
            print("\n❌ Instalación cancelada")
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    installer = QuickInstaller()
    installer.run()