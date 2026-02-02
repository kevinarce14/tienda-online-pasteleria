import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

# Obtener DATABASE_URL de variables de entorno
# Si no existe, usar Neon (tu configuración actual)
DATABASE_URL_STRING = os.getenv("DATABASE_URL")

if DATABASE_URL_STRING:
    # Si viene de variable de entorno (Vercel, Heroku, etc.)
    # Fix para postgres:// vs postgresql://
    if DATABASE_URL_STRING.startswith("postgres://"):
        DATABASE_URL_STRING = DATABASE_URL_STRING.replace("postgres://", "postgresql://", 1)
    
    engine = create_engine(
        DATABASE_URL_STRING,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={"sslmode": "require"} if "neon" in DATABASE_URL_STRING or "render" in DATABASE_URL_STRING else {}
    )
else:
    # Configuración local/Neon hardcoded como fallback
    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER", "neondb_owner"),
        password=os.getenv("DB_PASSWORD", "npg_gRD2wkVuvYH4"),
        host=os.getenv("DB_HOST", "ep-wispy-breeze-acjxjbvm.sa-east-1.aws.neon.tech"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "neondb"),
        query={
            "sslmode": "require",
            "options": f"-c search_path={os.getenv('DB_SCHEMA', 'pasteleria')}"
        }
    )
    
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()