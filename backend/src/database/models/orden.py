from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from backend.src.database.db import Base

class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True, index=True)
    nombre_cliente = Column(String(150))
    email_cliente = Column(String(150))
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(30), default="pendiente")
    fecha_creacion = Column(DateTime, server_default=func.now())

