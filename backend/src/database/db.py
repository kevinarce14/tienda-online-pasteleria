# backend/src/database/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def get_database_url():
    """
    Obtiene la URL de la base de datos según el entorno
    """
    # 1. Primero intentar variable de entorno directa
    db_url = os.environ.get("DATABASE_URL")
    
    if db_url:
        return db_url
    
    # 2. Si no, estamos en desarrollo - cargar dotenv
    try:
        from dotenv import load_dotenv
        
        # Intentar cargar desde diferentes rutas
        current_dir = os.path.dirname(__file__)
        possible_paths = [
            os.path.join(current_dir, "../../../.env"),  # Desde db.py hacia raíz
            os.path.join(current_dir, "../../.env"),
            ".env"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                load_dotenv(path)
                print(f"Desarrollo: Cargado .env desde {path}")
                break
        
        db_url = os.environ.get("DATABASE_URL")
        if db_url:
            return db_url
            
    except ImportError:
        pass  # dotenv no instalado
    
    
    return f"postgresql no encontrado"

# Obtener URL
DATABASE_URL_STRING = get_database_url()

if not DATABASE_URL_STRING:
    raise ValueError("No se pudo obtener la URL de la base de datos")

# Fix formato
if DATABASE_URL_STRING.startswith("postgres://"):
    DATABASE_URL_STRING = DATABASE_URL_STRING.replace("postgres://", "postgresql://", 1)

# Crear engine
engine = create_engine(
    DATABASE_URL_STRING,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"sslmode": "require"} if "neon" in DATABASE_URL_STRING else {}
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