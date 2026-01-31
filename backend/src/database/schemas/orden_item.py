from pydantic import BaseModel, Field
from decimal import Decimal


class OrdenItemCreate(BaseModel):
    producto_id: int | None
    nombre_producto: str
    precio_unitario: Decimal = Field(gt=0)
    cantidad: int = Field(gt=0)

class OrdenItemResponse(BaseModel):
    id: int
    producto_id: int | None
    nombre_producto: str
    precio_unitario: Decimal
    cantidad: int
    subtotal: Decimal

    class Config:
        from_attributes = True