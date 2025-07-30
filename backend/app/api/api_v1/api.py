from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users, surveys, evaluations

api_router = APIRouter()

# Incluir todas las rutas de endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["autenticacion"])
api_router.include_router(users.router, prefix="/users", tags=["usuarios"])
api_router.include_router(surveys.router, prefix="/surveys", tags=["encuestas"])
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["evaluaciones"])