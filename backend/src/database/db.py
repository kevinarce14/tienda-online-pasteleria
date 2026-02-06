import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# En Vercel, NO uses load_dotenv() - las variables ya están en el entorno
# load_dotenv()  # <- COMENTA o ELIMINA esta línea

# Obtener DATABASE_URL de variables de entorno de Vercel
DATABASE_URL_STRING = os.getenv("DATABASE_URL")

if not DATABASE_URL_STRING:
    # Para debugging en Vercel
    print("DEBUG: DATABASE_URL no encontrada en variables de entorno")
    print("DEBUG: Variables disponibles:", [k for k in os.environ.keys() if 'DATABASE' in k or 'POSTGRES' in k])
    raise ValueError("DATABASE_URL no está configurada en las variables de entorno")

# Fix para postgres:// vs postgresql:// (por si acaso)
if DATABASE_URL_STRING.startswith("postgres://"):
    DATABASE_URL_STRING = DATABASE_URL_STRING.replace("postgres://", "postgresql://", 1)

# Crear engine
engine = create_engine(
    DATABASE_URL_STRING,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"sslmode": "require"}
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