from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = URL.create(
    drivername="postgresql",
    username="postgres",
    password="SqlKevin",
    host="localhost",
    database="db-tienda-online-pasteleria",
    port=5432,
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# -------------------------
# Dependency DB
# -------------------------
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