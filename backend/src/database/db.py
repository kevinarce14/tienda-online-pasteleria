from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = URL.create(
#     drivername="postgresql",
#     username="postgres",
#     password="SqlKevin",
#     host="localhost",
#     database="db-tienda-online-pasteleria",
#     port=5432
# )
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="neondb_owner",
    password="npg_gRD2wkVuvYH4",
    host="ep-wispy-breeze-acjxjbvm.sa-east-1.aws.neon.tech",
    port=5432,
    database="neondb",
    query={
        "sslmode": "require",
        "options": "-c search_path=pasteleria"
    }
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
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





# from sqlalchemy import create_engine
# from sqlalchemy.engine import URL
# from sqlalchemy.orm import sessionmaker

# url = URL.create(
#     drivername="postgresql",
#     username="postgres",
#     password="SqlKevin",
#     host="localhost",
#     database="db-tienda-online-pasteleria",
#     port=5432,
# )

# engine = create_engine(url)
# Session = sessionmaker(bind=engine)
# session = Session()