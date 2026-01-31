from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, DateTime
from sqlalchemy.sql import func

from database.db import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    precio = Column(DECIMAL(10, 2), nullable=False)
    imagen_url = Column(Text)
    categoria = Column(String(50), default="wedding_cake")

    disponible = Column(Boolean, default=True)
    destacado = Column(Boolean, default=False)
    stock = Column(Integer, nullable=True)  # NULL = bajo pedido / ilimitado

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now())
