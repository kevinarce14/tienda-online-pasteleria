from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from sqlalchemy.sql import func
from backend.src.database.db import Base

class ConsultaCustom(Base):
    __tablename__ = "consultas_custom"
    __table_args__ = {"schema": "pasteleria"}    

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    fecha_evento = Column(Date, nullable=False)
    invitados = Column(String(50))
    detalles = Column(Text)
    estado = Column(String(30), default="nueva")
    fecha_creacion = Column(DateTime, server_default=func.now())
