# Manual Completo - Sistema de Evaluación Docente
## Guía Exhaustiva de Instalación, Configuración y Uso

---

## 📋 ÍNDICE

1. [Introducción y Visión General](#introducción)
2. [Requisitos del Sistema](#requisitos)
3. [Instalación Automática](#instalación-automática)
4. [Instalación Manual](#instalación-manual)
5. [Configuración Avanzada](#configuración-avanzada)
6. [Solución de Problemas](#solución-de-problemas)
7. [Casos de Uso Específicos](#casos-de-uso)
8. [Mantenimiento y Actualización](#mantenimiento)
9. [Seguridad y Backup](#seguridad)
10. [Escalabilidad y Migración](#escalabilidad)

---

## 🎯 INTRODUCCIÓN

### ¿Qué es el Sistema de Evaluación Docente?

Sistema completo para la evaluación integral del desempeño docente que permite:

- **Autoevaluación**: Los maestros evalúan su propio desempeño
- **Evaluación por coordinadores**: Supervisores evalúan a los maestros
- **Análisis comparativo**: Identifica diferencias entre percepciones
- **Reportes y métricas**: Dashboard con estadísticas y tendencias

### Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│    Frontend     │    │     Backend      │    │   Base de       │
│    (React)      │◄──►│    (FastAPI)     │◄──►│   Datos         │
│  Port: 3000     │    │   Port: 8000     │    │ (PostgreSQL)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Modos de Deployment

| Modo | Descripción | Acceso | Seguridad | Uso Recomendado |
|------|-------------|--------|-----------|-----------------|
| **Local** | Solo red interna | LAN únicamente | Máxima | Instituciones con políticas estrictas |
| **Híbrido** | Local + Web opcional | LAN + Internet | Alta | Instituciones que necesitan flexibilidad |

---

## 💻 REQUISITOS DEL SISTEMA

### Requisitos Mínimos

#### Hardware
- **CPU**: 2 cores, 2.0 GHz
- **RAM**: 4 GB mínimo, 8 GB recomendado
- **Almacenamiento**: 10 GB libres
- **Red**: Conexión estable (para instalación)

#### Software Base
- **Python**: 3.11 o superior
- **PostgreSQL**: 12 o superior
- **Sistema Operativo**: Windows 10+, macOS 10.15+, Ubuntu 20.04+

#### Software Opcional
- **Node.js**: 18+ (para desarrollo frontend)
- **Git**: Para control de versiones
- **pgAdmin**: Interface gráfica para PostgreSQL

### Verificación de Requisitos

#### Windows
```cmd
# Verificar Python
python --version

# Verificar PostgreSQL
psql --version

# Verificar Node.js (opcional)
node --version
```

#### Linux/macOS
```bash
# Verificar Python
python3 --version

# Verificar PostgreSQL
psql --version

# Verificar Node.js (opcional)
node --version
```

### Instalación de Requisitos

#### Windows

**Python 3.11+:**
1. Descargar desde https://www.python.org/downloads/windows/
2. ✅ Marcar "Add Python to PATH"
3. Instalar con "Install Now"

**PostgreSQL:**
1. Descargar desde https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
2. Instalar con configuración por defecto
3. Recordar el password del usuario 'postgres'

**Node.js (Opcional):**
1. Descargar desde https://nodejs.org/en/download/
2. Instalar con configuración por defecto

#### macOS

```bash
# Instalar Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python@3.11

# Instalar PostgreSQL
brew install postgresql
brew services start postgresql

# Instalar Node.js (opcional)
brew install node
```

#### Ubuntu/Debian

```bash
# Actualizar sistema
sudo apt update

# Instalar Python 3.11
sudo apt install python3.11 python3.11-pip python3.11-venv

# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib

# Instalar Node.js (opcional)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## 🚀 INSTALACIÓN AUTOMÁTICA

### Script Master - Un Solo Comando

El script `install_complete_system.py` instala automáticamente:
- ✅ Estructura completa del proyecto
- ✅ Todos los archivos de código
- ✅ Configuración personalizada
- ✅ Base de datos con datos iniciales
- ✅ Dependencias del backend
- ✅ Scripts de inicio

### Ejecución del Script Master

#### Paso 1: Descargar el Script
```bash
# Crear directorio del proyecto
mkdir evaluacion-docente
cd evaluacion-docente

# Copiar el script install_complete_system.py al directorio
```

#### Paso 2: Ejecutar Instalación
```bash
python install_complete_system.py
```

#### Paso 3: Seguir el Asistente Interactivo

El script te preguntará:

1. **Información de la Institución**
   ```
   📚 Nombre completo: Universidad Ejemplo
   📝 Nombre corto: universidad_ejemplo
   ```

2. **Modo de Red**
   ```
   1. Solo red local (LAN) - Más seguro
   2. Híbrido (LAN + web) - Más flexible
   ```

3. **Configuración de PostgreSQL**
   ```
   Host: localhost
   Puerto: 5432
   Usuario: postgres
   Password: [tu_password]
   ```

4. **Usuario Administrador**
   ```
   Email: admin@universidad.edu
   Password: admin123
   Nombre: Admin
   Apellido: Sistema
   ```

#### Paso 4: Verificar Instalación

Al finalizar verás:
```
🎉 INSTALACIÓN COMPLETADA

📋 RESUMEN:
   • Institución: Universidad Ejemplo
   • Modo de red: local
   • Base de datos: evaluacion_universidad_ejemplo
   • Admin: admin@universidad.edu

🚀 PARA INICIAR:
   Windows: iniciar_sistema.bat
   Linux/Mac: ./iniciar_sistema.sh
```

### Posibles Problemas en Instalación Automática

#### Error: "PostgreSQL no encontrado"
**Causa**: PostgreSQL no está en el PATH
**Solución**:
```bash
# Windows: Agregar al PATH
C:\Program Files\PostgreSQL\15\bin

# Linux/macOS: Instalar PostgreSQL
sudo apt install postgresql  # Ubuntu
brew install postgresql      # macOS
```

#### Error: "No se puede conectar a la base de datos"
**Causa**: Credenciales incorrectas o servicio no iniciado
**Solución**:
```bash
# Verificar servicio PostgreSQL
# Windows: Servicios > PostgreSQL
# Linux: sudo systemctl start postgresql
# macOS: brew services start postgresql

# Verificar conexión
psql -U postgres -h localhost
```

#### Error: "Permisos insuficientes"
**Causa**: No tienes permisos para crear archivos
**Solución**:
```bash
# Cambiar permisos del directorio
chmod 755 evaluacion-docente

# O ejecutar como administrador (Windows)
# Clic derecho > "Ejecutar como administrador"
```

---

## 🔧 INSTALACIÓN MANUAL

### Cuándo Usar Instalación Manual

- El script automático falla
- Necesitas control granular
- Quieres entender cada paso
- Configuración personalizada extrema

### Paso 1: Crear Estructura de Directorios

```bash
mkdir -p evaluacion-docente/{backend/app/{core,models,schemas,api/api_v1/endpoints,services,utils},frontend/{public,src/{components/{auth,common,layout},pages/{admin,coordinator,teacher,common},contexts,services,utils,hooks}},database/{migrations,backups,scripts},docs,tools,logs,config}
```

### Paso 2: Crear Archivos Base

#### Backend - requirements.txt
```txt
fastapi==0.104.1
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
httpx==0.25.2
```

#### Frontend - package.json
```json
{
  "name": "evaluacion-docente-frontend",
  "version": "1.0.0",
  "private": true,
  "homepage": "./",
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
    "date-fns": "^2.29.3",
    "@headlessui/react": "^1.7.14",
    "clsx": "^1.2.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "proxy": "http://localhost:8000"
}
```

### Paso 3: Copiar Código de Artifacts

Copiar el contenido de cada artifact creado anteriormente a su archivo correspondiente:

- `backend_config` → `backend/app/core/config.py`
- `backend_main` → `backend/app/main.py`  
- `database_schema` → `database/01_create_schema.sql`
- Y así sucesivamente...

### Paso 4: Configurar Base de Datos

```bash
# Crear base de datos
createdb -U postgres evaluacion_mi_institucion

# Ejecutar scripts
psql -U postgres -d evaluacion_mi_institucion -f database/01_create_schema.sql
psql -U postgres -d evaluacion_mi_institucion -f database/02_insert_seeds.sql
```

### Paso 5: Instalar Dependencias

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### Paso 6: Configurar Variables de Entorno

Crear `.env`:
```bash
INSTITUTION_NAME=Mi Institución
INSTITUTION_SHORT=mi_institucion
NETWORK_MODE=local
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=mi_password
DB_NAME=evaluacion_mi_institucion
SECRET_KEY=mi_clave_super_secreta
ADMIN_EMAIL=admin@mi-institucion.edu
ADMIN_PASSWORD=admin123
ADMIN_FIRST_NAME=Admin
ADMIN_LAST_NAME=Sistema
```

---

## ⚙️ CONFIGURACIÓN AVANZADA

### Configuración de Red

#### Modo Local Estricto
```bash
# .env
NETWORK_MODE=local
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://192.168.1.100:3000"]
```

#### Modo Híbrido
```bash
# .env
NETWORK_MODE=hybrid
ENABLE_WEB_ACCESS=true
WEB_DOMAIN=evaluacion.mi-institucion.edu
SSL_ENABLED=true
BACKEND_CORS_ORIGINS=["http://localhost:3000","https://evaluacion.mi-institucion.edu"]
```

### Configuración de Seguridad

#### JWT Personalizado
```bash
# Generar clave segura
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Configurar en .env
SECRET_KEY=tu_clave_generada_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=480  # 8 horas
```

#### Configuración de HTTPS

Para modo híbrido con SSL:

1. **Obtener certificado SSL**
   ```bash
   # Let's Encrypt (recomendado)
   sudo apt install certbot
   sudo certbot certonly --standalone -d evaluacion.mi-institucion.edu
   ```

2. **Configurar proxy reverso (Nginx)**
   ```nginx
   server {
       listen 443 ssl;
       server_name evaluacion.mi-institucion.edu;
       
       ssl_certificate /etc/letsencrypt/live/evaluacion.mi-institucion.edu/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/evaluacion.mi-institucion.edu/privkey.pem;
       
       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Configuración de Base de Datos

#### PostgreSQL Optimizado

**postgresql.conf**:
```conf
# Configuración para sistema de evaluación docente
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100

# Logging para auditoría
log_destination = 'stderr'
logging_collector = on
log_directory = 'logs'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_statement = 'mod'  # Log modificaciones (INSERT, UPDATE, DELETE)
```

**pg_hba.conf**:
```conf
# Configuración de acceso
local   all             postgres                                peer
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
# Para acceso desde red local (opcional)
host    all             all             192.168.1.0/24          md5
```

#### Backup Automático

**Script backup diario**:
```bash
#!/bin/bash
# backup_daily.sh

DB_NAME="evaluacion_mi_institucion"
BACKUP_DIR="/backups/evaluacion"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Backup con compresión
pg_dump -U postgres -h localhost $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Mantener solo últimos 30 backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completado: backup_$DATE.sql.gz"
```

### Personalización de la Institución

#### Logo y Colores Personalizados

**frontend/src/config/institution.js**:
```javascript
export const institutionConfig = {
  name: "Universidad Ejemplo",
  shortName: "UE",
  logo: "/assets/logo-institucion.png",
  favicon: "/assets/favicon.ico",
  colors: {
    primary: "#1e40af",      // Azul institucional
    secondary: "#64748b",    // Gris
    accent: "#059669",       // Verde para éxito
    danger: "#dc2626"        // Rojo para errores
  },
  theme: {
    defaultMode: "light",    // light, dark, auto
    allowToggle: true
  },
  contact: {
    email: "soporte@universidad.edu",
    phone: "+1 (555) 123-4567",
    address: "123 Calle Universidad, Ciudad, País"
  }
};
```

#### Personalización de Encuestas

**Plantillas predefinidas**:
```sql
-- Encuesta para educación básica
INSERT INTO surveys (title, description, instructions) VALUES 
('Evaluación Docente - Educación Básica',
 'Evaluación específica para maestros de primaria',
 'Califique considerando las competencias específicas de educación básica');

-- Encuesta para educación superior  
INSERT INTO surveys (title, description, instructions) VALUES 
('Evaluación Docente - Educación Superior',
 'Evaluación para profesores universitarios',
 'Incluye criterios de investigación y extensión universitaria');
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Problemas Comunes de Instalación

#### 1. Error: "ModuleNotFoundError: No module named 'app'"

**Síntomas**:
```bash
ModuleNotFoundError: No module named 'app'
```

**Causas**:
- Estructura de directorios incorrecta
- Archivos `__init__.py` faltantes
- PYTHONPATH incorrecto

**Soluciones**:
```bash
# Verificar estructura
ls -la backend/app/
# Debe mostrar __init__.py

# Crear archivos faltantes
touch backend/app/__init__.py
touch backend/app/core/__init__.py
touch backend/app/models/__init__.py

# Ejecutar desde directorio correcto
cd backend
python -m uvicorn app.main:app --reload
```

#### 2. Error: "CORS policy" en el navegador

**Síntomas**:
```
Access to XMLHttpRequest blocked by CORS policy
```

**Causas**:
- Configuración CORS incorrecta
- Frontend y backend en puertos diferentes
- URL incorrecta en el frontend

**Soluciones**:
```bash
# Verificar configuración CORS en .env
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# Verificar URL de API en frontend
# frontend/src/services/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

# Reiniciar servicios
pkill -f uvicorn
pkill -f "npm start"
```

#### 3. Error: "Database connection failed"

**Síntomas**:
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Causas**:
- PostgreSQL no está ejecutándose
- Credenciales incorrectas
- Base de datos no existe

**Soluciones**:
```bash
# Verificar servicio PostgreSQL
sudo systemctl status postgresql  # Linux
brew services list | grep postgres  # macOS

# Iniciar PostgreSQL
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS

# Verificar conexión manual
psql -U postgres -h localhost -c "SELECT version();"

# Recrear base de datos si es necesario
dropdb -U postgres evaluacion_mi_institucion
createdb -U postgres evaluacion_mi_institucion
```

#### 4. Error: "Port already in use"

**Síntomas**:
```
Error: listen EADDRINUSE: address already in use :::8000
```

**Soluciones**:
```bash
# Encontrar proceso usando el puerto
lsof -ti:8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Terminar proceso
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# O cambiar puerto en configuración
# backend: uvicorn app.main:app --port 8001
# frontend: PORT=3001 npm start
```

### Problemas de Performance

#### 1. Frontend Lento

**Optimizaciones**:
```javascript
// React.lazy para componentes grandes
const AdminUsers = React.lazy(() => import('./pages/admin/Users'));

// Memo para componentes que no cambian frecuentemente
const UserCard = React.memo(({ user }) => {
  return <div>{user.name}</div>;
});

// Virtualización para listas grandes
import { FixedSizeList as List } from 'react-window';
```

#### 2. Backend Lento

**Optimizaciones**:
```python
# Índices de base de datos
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
CREATE INDEX CONCURRENTLY idx_evaluations_status ON evaluations(status);

# Paginación en consultas
@router.get("/users")
async def get_users(page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    users = db.query(User).offset(offset).limit(limit).all()
    return users

# Cache con Redis (opcional)
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
```

### Problemas de Seguridad

#### 1. Configurar Firewall

**Linux (UFW)**:
```bash
# Permitir solo puertos necesarios
sudo ufw allow 22    # SSH
sudo ufw allow 5432  # PostgreSQL (solo si acceso externo)
sudo ufw allow 8000  # Backend (solo si acceso externo)
sudo ufw allow 3000  # Frontend (solo si acceso externo)
sudo ufw enable
```

**Windows Firewall**:
```cmd
# Abrir Firewall de Windows Defender
# Reglas de entrada > Nueva regla > Puerto
# TCP, puertos específicos: 8000, 3000
```

#### 2. Configurar HTTPS (Producción)

**Con Let's Encrypt**:
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d evaluacion.mi-institucion.edu

# Renovación automática
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 💼 CASOS DE USO ESPECÍFICOS

### Caso 1: Institución Pequeña (< 50 usuarios)

**Configuración Recomendada**:
```bash
# Hardware mínimo
RAM: 4GB
CPU: 2 cores
Almacenamiento: 20GB

# Configuración
NETWORK_MODE=local
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 horas
```

**Ventajas**:
- Setup simple
- Mantenimiento mínimo
- Costos bajos

### Caso 2: Institución Mediana (50-200 usuarios)

**Configuración Recomendada**:
```bash
# Hardware recomendado
RAM: 8GB
CPU: 4 cores
Almacenamiento: 50GB

# Configuración
NETWORK_MODE=hybrid
ENABLE_WEB_ACCESS=true
```

**Consideraciones adicionales**:
- Backup automático diario
- Monitoreo básico
- Acceso remoto para coordinadores

### Caso 3: Institución Grande (200+ usuarios)

**Configuración Recomendada**:
```bash
# Hardware profesional
RAM: 16GB+
CPU: 8+ cores
Almacenamiento: 100GB+ SSD

# Configuración
NETWORK_MODE=hybrid
ENABLE_WEB_ACCESS=true
SSL_ENABLED=true
```

**Implementaciones adicionales**:
- Load balancer
- Base de datos replicada
- Backup en tiempo real
- Monitoreo avanzado

### Caso 4: Múltiples Campus

**Opción A: Instancia Central**
```bash
# Una instalación para todos los campus
# Diferenciación por departamentos
```

**Opción B: Instancias Separadas**
```bash
# Una instalación por campus
# Sincronización manual o automática
```

**Script de Sincronización**:
```python
#!/usr/bin/env python3
"""
Script para sincronizar datos entre campus
"""
import psycopg2
import json

def sync_campus_data():
    # Conectar a campus principal
    main_db = psycopg2.connect(
        host="main.universidad.edu",
        database="evaluacion_principal",
        user="sync_user",
        password="sync_password"
    )
    
    # Conectar a campus secundario
    branch_db = psycopg2.connect(
        host="branch.universidad.edu", 
        database="evaluacion_branch",
        user="sync_user",
        password="sync_password"
    )
    
    # Sincronizar usuarios, encuestas, etc.
    # ... lógica de sincronización
```

---

## 🔧 MANTENIMIENTO Y ACTUALIZACIÓN

### Rutinas de Mantenimiento

#### Diario
```bash
#!/bin/bash
# mantenimiento_diario.sh

# Backup de base de datos
pg_dump evaluacion_mi_institucion > /backups/daily_$(date +%Y%m%d).sql

# Limpiar logs antiguos
find /var/log/evaluacion -name "*.log" -mtime +7 -delete

# Verificar espacio en disco
df -h | grep -E "/$|/var"

# Verificar servicios
systemctl is-active postgresql
systemctl is-active nginx  # Si usas proxy
```

#### Semanal
```bash
#!/bin/bash
# mantenimiento_semanal.sh

# Vacuum de base de datos
psql -U postgres -d evaluacion_mi_institucion -c "VACUUM ANALYZE;"

# Verificar integridad de backup
pg_restore --list /backups/latest_backup.sql > /dev/null

# Verificar actualizaciones de seguridad
apt list --upgradable | grep -i security
```

#### Mensual
```bash
#!/bin/bash
# mantenimiento_mensual.sh

# Backup completo
pg_dump -Fc evaluacion_mi_institucion > /backups/monthly_$(date +%Y%m).backup

# Análisis de rendimiento
psql -U postgres -d evaluacion_mi_institucion -c "
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;"

# Revisar logs de errores
grep -i error /var/log/evaluacion/*.log | tail -50
```

### Actualización del Sistema

#### Actualización Menor (Bug fixes)
```bash
# 1. Backup de datos
pg_dump evaluacion_mi_institucion > backup_pre_update.sql

# 2. Actualizar código
git pull origin main  # Si usas Git
# O reemplazar archivos manualmente

# 3. Actualizar dependencias
cd backend && pip install -r requirements.txt --upgrade
cd frontend && npm update

# 4. Reiniciar servicios
sudo systemctl restart evaluacion-backend
sudo systemctl restart evaluacion-frontend
```

#### Actualización Mayor (Nuevas características)
```bash
# 1. Backup completo
pg_dump -Fc evaluacion_mi_institucion > backup_major_update.backup

# 2. Ejecutar migraciones de BD
psql -U postgres -d evaluacion_mi_institucion -f migrations/v2.0.sql

# 3. Actualizar configuración
cp .env .env.backup
# Revisar nuevas variables en .env.example

# 4. Pruebas en entorno de desarrollo
# Verificar funcionalidad antes de producción

# 5. Despliegue en producción
```

### Monitoreo del Sistema

#### Script de Monitoreo Básico
```python
#!/usr/bin/env python3
"""
Script de monitoreo para el sistema de evaluación
"""
import psutil
import psycopg2
import requests
import smtplib
from email.mime.text import MIMEText

def check_system_health():
    issues = []
    
    # Verificar CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > 80:
        issues.append(f"CPU alta: {cpu_percent}%")
    
    # Verificar memoria
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        issues.append(f"Memoria alta: {memory.percent}%")
    
    # Verificar disco
    disk = psutil.disk_usage('/')
    if disk.percent > 80:
        issues.append(f"Disco lleno: {disk.percent}%")
    
    # Verificar PostgreSQL
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="evaluacion_mi_institucion",
            user="postgres"
        )
        conn.close()
    except:
        issues.append("PostgreSQL no accesible")
    
    # Verificar API
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            issues.append("API no responde correctamente")
    except:
        issues.append("API no accesible")
    
    # Verificar Frontend
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code != 200:
            issues.append("Frontend no accesible")
    except:
        issues.append("Frontend no accesible")
    
    return issues

def send_alert(issues):
    if not issues:
        return
        
    message = "Problemas detectados en el sistema:\n\n"
    for issue in issues:
        message += f"- {issue}\n"
    
    # Enviar email (configurar SMTP)
    msg = MIMEText(message)
    msg['Subject'] = 'Alerta: Sistema de Evaluación Docente'
    msg['From'] = 'sistema@mi-institucion.edu'
    msg['To'] = 'admin@mi-institucion.edu'
    
    # smtp_server.send_message(msg)

if __name__ == "__main__":
    issues = check_system_health()
    if issues:
        send_alert(issues)
        print("Alertas enviadas")
    else:
        print("Sistema funcionando correctamente")
```

---

## 🔒 SEGURIDAD Y BACKUP

### Estrategia de Backup

#### Backup 3-2-1
- **3** copias de los datos
- **2** medios diferentes
- **1** copia fuera del sitio

```bash
#!/bin/bash
# estrategia_backup_321.sh

DB_NAME="evaluacion_mi_institucion"
LOCAL_BACKUP="/backups/local"
NETWORK_BACKUP="/mnt/nas/backups"
CLOUD_BACKUP="s3://mi-bucket/backups"

# Backup local (1ra copia)
pg_dump -Fc $DB_NAME > $LOCAL_BACKUP/backup_$(date +%Y%m%d).backup

# Backup en red (2da copia, 2do medio)
cp $LOCAL_BACKUP/backup_$(date +%Y%m%d).backup $NETWORK_BACKUP/

# Backup en la nube (3ra copia, fuera del sitio)
aws s3 cp $LOCAL_BACKUP/backup_$(date +%Y%m%d).backup $CLOUD_BACKUP/
```

#### Restauración de Backup
```bash
#!/bin/bash
# restaurar_backup.sh

BACKUP_FILE="$1"
DB_NAME="evaluacion_mi_institucion"

if [ -z "$BACKUP_FILE" ]; then
    echo "Uso: $0 <archivo_backup>"
    exit 1
fi

# Confirmar restauración
read -p "¿Restaurar $BACKUP_FILE a $DB_NAME? (y/N): " confirm
if [ "$confirm" != "y" ]; then
    echo "Operación cancelada"
    exit 0
fi

# Backup actual antes de restaurar
pg_dump -Fc $DB_NAME > backup_before_restore_$(date +%Y%m%d_%H%M).backup

# Eliminar conexiones activas
psql -U postgres -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = '$DB_NAME' AND pid <> pg_backend_pid();"

# Restaurar
dropdb -U postgres $DB_NAME
createdb -U postgres $DB_NAME
pg_restore -U postgres -d $DB_NAME $BACKUP_FILE

echo "Restauración completada"
```

### Configuración de Seguridad Avanzada

#### Encriptación de Datos

**Encriptación en tránsito (SSL/TLS)**:
```bash
# PostgreSQL con SSL
# postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
ssl_ca_file = 'ca.crt'
```

**Encriptación en reposo**:
```bash
# Encriptación de disco (Linux)
sudo cryptsetup luksFormat /dev/sdb1
sudo cryptsetup luksOpen /dev/sdb1 encrypted_disk
sudo mkfs.ext4 /dev/mapper/encrypted_disk
```

#### Auditoría y Logging

**Configuración de auditoría PostgreSQL**:
```sql
-- Instalar extensión de auditoría
CREATE EXTENSION IF NOT EXISTS pgaudit;

-- Configurar auditoría
ALTER SYSTEM SET pgaudit.log = 'write,ddl';
ALTER SYSTEM SET pgaudit.log_catalog = off;
ALTER SYSTEM SET pgaudit.log_parameter = on;
SELECT pg_reload_conf();
```

**Logs de aplicación**:
```python
import logging
import logging.handlers
import os

# Configurar logging robusto
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Configurar formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para archivos rotativos
    file_handler = logging.handlers.RotatingFileHandler(
        f'{log_dir}/evaluacion.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Handler para errores críticos
    error_handler = logging.handlers.SMTPHandler(
        mailhost='smtp.mi-institucion.edu',
        fromaddr='sistema@mi-institucion.edu',
        toaddrs=['admin@mi-institucion.edu'],
        subject='Error Crítico - Sistema Evaluación'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    # Configurar logger principal
    logger = logging.getLogger('evaluacion')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    return logger
```

---

## 📈 ESCALABILIDAD Y MIGRACIÓN

### Escalabilidad Horizontal

#### Load Balancer con Nginx
```nginx
upstream backend_servers {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

upstream frontend_servers {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

server {
    listen 80;
    server_name evaluacion.mi-institucion.edu;
    
    location /api {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location / {
        proxy_pass http://frontend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Base de Datos Distribuida

**Master-Slave Replication**:
```bash
# Configuración Master (postgresql.conf)
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 32
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/archive/%f'

# Configuración Slave
standby_mode = 'on'
primary_conninfo = 'host=master_ip port=5432 user=replicator'
trigger_file = '/var/lib/postgresql/trigger_file'
```

### Migración entre Versiones

#### Script de Migración
```python
#!/usr/bin/env python3
"""
Script de migración entre versiones del sistema
"""
import psycopg2
import json
import os
from pathlib import Path

class SystemMigrator:
    def __init__(self, old_version, new_version):
        self.old_version = old_version
        self.new_version = new_version
        
    def migrate_database(self):
        """Migrar esquema de base de datos"""
        migrations_dir = Path("migrations")
        
        # Buscar archivos de migración
        migration_files = sorted(
            migrations_dir.glob(f"v{self.old_version}_to_v{self.new_version}_*.sql")
        )
        
        for migration_file in migration_files:
            print(f"Ejecutando migración: {migration_file}")
            self.execute_sql_file(migration_file)
            
    def migrate_config(self):
        """Migrar archivo de configuración"""
        old_config = self.load_config(".env")
        new_config = self.update_config_schema(old_config)
        self.save_config(".env.new", new_config)
        
    def migrate_data(self):
        """Migrar datos específicos"""
        # Lógica específica según la migración
        pass
        
    def execute_sql_file(self, file_path):
        """Ejecutar archivo SQL"""
        conn = psycopg2.connect("postgresql://...")
        with open(file_path, 'r') as f:
            conn.cursor().execute(f.read())
        conn.commit()
        conn.close()

# Uso
migrator = SystemMigrator("1.0", "2.0")
migrator.migrate_database()
migrator.migrate_config()
migrator.migrate_data()
```

### Containerización con Docker

#### Docker Compose Completo
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: evaluacion_docente
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres123
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3

  backend:
    build: ./backend
    environment:
      - DB_HOST=db
      - DB_PORT=5432
      - DB_USER=postgres
      - DB_PASSWORD=postgres123
      - DB_NAME=evaluacion_docente
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./backend:/app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
```

---

## 📞 SOPORTE Y CONTACTO

### Canales de Soporte

#### Nivel 1: Documentación
- Manual completo (este documento)
- README.md del proyecto
- Documentación API: http://localhost:8000/docs

#### Nivel 2: Auto-diagnóstico
```bash
# Script de diagnóstico
python tools/system_diagnostic.py
```

#### Nivel 3: Logs del Sistema
```bash
# Logs del backend
tail -f logs/evaluacion.log

# Logs de PostgreSQL
tail -f /var/log/postgresql/postgresql-*.log

# Logs del sistema
journalctl -u evaluacion-backend -f
```

### Resolución de Problemas Avanzados

#### Performance Issues
1. **Verificar consultas lentas**:
   ```sql
   SELECT query, calls, total_time, mean_time
   FROM pg_stat_statements
   ORDER BY total_time DESC
   LIMIT 10;
   ```

2. **Optimizar índices**:
   ```sql
   SELECT schemaname, tablename, attname, n_distinct, correlation
   FROM pg_stats
   WHERE tablename = 'evaluations';
   ```

#### Problemas de Memoria
```bash
# Monitorear memoria en tiempo real
watch -n 1 'free -h && echo && ps aux --sort=-%mem | head -10'

# Optimizar PostgreSQL
# postgresql.conf
shared_buffers = 25% of RAM
effective_cache_size = 75% of RAM
```

### Contacto para Desarrollo Personalizado

Para personalizaciones específicas, integraciones o soporte profesional:

- **Email**: desarrollo@sistema-evaluacion.com
- **Documentación técnica**: Disponible en el proyecto
- **Issues y mejoras**: GitHub/GitLab del proyecto

---

## 📄 APÉNDICES

### Apéndice A: Códigos de Error Comunes

| Código | Descripción | Solución |
|--------|-------------|----------|
| E001 | Error de conexión PostgreSQL | Verificar servicio y credenciales |
| E002 | Puerto en uso | Cambiar puerto o liberar el actual |
| E003 | Módulo Python faltante | `pip install -r requirements.txt` |
| E004 | Error CORS | Verificar BACKEND_CORS_ORIGINS |
| E005 | JWT inválido | Verificar SECRET_KEY |

### Apéndice B: Comandos de Mantenimiento

```bash
# Backup rápido
pg_dump evaluacion_mi_institucion > backup_$(date +%Y%m%d).sql

# Restaurar backup
psql -U postgres evaluacion_mi_institucion < backup.sql

# Reiniciar servicios
sudo systemctl restart postgresql
pkill -f uvicorn && cd backend && python -m uvicorn app.main:app &

# Verificar salud del sistema
curl http://localhost:8000/health
curl http://localhost:3000
```

### Apéndice C: Estructura de Base de Datos

Ver archivo `database/01_create_schema.sql` para esquema completo.

**Tablas principales**:
- `users`: Usuarios del sistema
- `roles`: Roles (admin, coordinador, maestro)
- `departments`: Departamentos/áreas
- `surveys`: Encuestas
- `questions`: Preguntas de encuestas
- `evaluations`: Evaluaciones realizadas
- `answers`: Respuestas individuales

---

**Versión del Manual**: 1.0  
**Fecha**: 2025  
**Compatibilidad**: Todas las versiones del sistema  
**Actualizado**: Con cada versión mayor del sistema