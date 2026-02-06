from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime
from sqlalchemy.sql import func
from backend.src.database.db import Base

class Producto(Base):
    __tablename__ = "productos"
    __table_args__ = {"schema": "pasteleria"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2), nullable=False)
    imagen_url = Column(Text)
    categoria = Column(String(50), default="wedding_cake")
    disponible = Column(Boolean, default=True)
    destacado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, server_default=func.now())
