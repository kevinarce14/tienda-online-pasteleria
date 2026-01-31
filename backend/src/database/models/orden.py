from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    DECIMAL,
    ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database.db import Base


class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="SET NULL"))

    numero_orden = Column(String(50), unique=True, nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    estado = Column(String(50), default="pendiente")
    metodo_pago = Column(String(50))

    notas_cliente = Column(Text)
    notas_internas = Column(Text)

    fecha_evento = Column(Date)
    direccion_entrega = Column(Text)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now())

    cliente = relationship("Cliente", back_populates="ordenes")
