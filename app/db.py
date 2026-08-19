import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def get_database_url() -> str:
    # Intenta leer la URL de la nube; si no existe (local), usa SQLite como comodín
    url = os.getenv("DATABASE_URL", "sqlite:///sensorhub.db")
    
    # Render entrega la URL como "postgres://", pero SQLAlchemy 2.x exige el driver
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url

engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass