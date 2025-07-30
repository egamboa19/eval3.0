from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.api_v1.api import api_router
import os

# Crear aplicacion FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description=f"Sistema de Evaluacion Docente - {settings.INSTITUTION_NAME}",
)

# Configurar CORS para modo local/híbrido
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos del frontend en modo local
if settings.is_local_only:
    frontend_build_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "build")
    if os.path.exists(frontend_build_path):
        app.mount("/static", StaticFiles(directory=os.path.join(frontend_build_path, "static")), name="static")

# Incluir rutas de la API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": f"Sistema de Evaluacion Docente - {settings.INSTITUTION_NAME}",
        "version": "1.0.0",
        "institution": settings.INSTITUTION_NAME,
        "network_mode": settings.NETWORK_MODE,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "institution": settings.INSTITUTION_NAME,
        "network_mode": settings.NETWORK_MODE,
        "database": "connected"
    }

@app.get("/config")
async def get_public_config():
    """Configuración pública para el frontend"""
    return {
        "institution_name": settings.INSTITUTION_NAME,
        "network_mode": settings.NETWORK_MODE,
        "enable_web_access": settings.ENABLE_WEB_ACCESS
    }