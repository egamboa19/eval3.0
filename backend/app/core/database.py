from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Crear engine de base de datos
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == "development"
)

# Crear session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependency para obtener session de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()