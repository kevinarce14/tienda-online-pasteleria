from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.src.database.db import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    telefono = Column(String(20))
    direccion = Column(Text)
    ciudad = Column(String(100))
    codigo_postal = Column(String(20))
    pais = Column(String(100), default="Argentina")
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    notas = Column(Text)

    ordenes = relationship("Orden", back_populates="cliente")
