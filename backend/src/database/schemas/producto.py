from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str
    precio: Decimal
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    categoria: str = "wedding_cake"

class ProductoResponse(ProductoCreate):
    id: int

    class Config:
        from_attributes = True
