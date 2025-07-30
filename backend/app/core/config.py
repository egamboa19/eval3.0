from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Configuración de institución
    INSTITUTION_NAME: str = "Institución Educativa"
    INSTITUTION_SHORT: str = "institucion"
    NETWORK_MODE: str = "local"  # local, hybrid, web
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sistema de Evaluacion Docente"
    
    # Base de datos
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "ABC123"
    DB_NAME: str = "evaluacion_docente"
    
    # JWT
    SECRET_KEY: str = "tu_clave_super_secreta_aqui_cambiar_en_produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 horas para uso local
    
    # CORS - Configuración para local/híbrido
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    
    # Admin inicial
    ADMIN_EMAIL: str = "admin@institucion.local"
    ADMIN_PASSWORD: str = "admin123"
    ADMIN_FIRST_NAME: str = "Admin"
    ADMIN_LAST_NAME: str = "Sistema"
    
    # Entorno
    ENVIRONMENT: str = "production"
    
    # Configuración híbrida
    ENABLE_WEB_ACCESS: bool = False  # Se activa en modo híbrido
    WEB_DOMAIN: Optional[str] = None
    SSL_ENABLED: bool = False
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def is_hybrid_mode(self) -> bool:
        return self.NETWORK_MODE == "hybrid"
        
    @property
    def is_local_only(self) -> bool:
        return self.NETWORK_MODE == "local"
        
    def get_cors_origins(self) -> List[str]:
        """Obtener orígenes CORS según el modo de red"""
        origins = self.BACKEND_CORS_ORIGINS.copy()
        
        if self.is_hybrid_mode and self.WEB_DOMAIN:
            origins.extend([
                f"https://{self.WEB_DOMAIN}",
                f"http://{self.WEB_DOMAIN}"
            ])
            
        return origins
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()