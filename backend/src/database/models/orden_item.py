from sqlalchemy import Column, Integer, Numeric, ForeignKey, String
from backend.src.database.db import Base


class OrdenItem(Base):
    __tablename__ = "orden_items"
    __table_args__ = {"schema": "pasteleria"}

    id = Column(Integer, primary_key=True, index=True)

    orden_id = Column(
        Integer,
        ForeignKey("ordenes.id", ondelete="CASCADE"),
        nullable=False
    )

    producto_id = Column(
        Integer,
        ForeignKey("productos.id", ondelete="SET NULL"),
        nullable=True
    )

    nombre_producto = Column(String(150), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    subtotal = Column(Numeric(10, 2), nullable=False)
