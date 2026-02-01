from pydantic import BaseModel, EmailStr
from decimal import Decimal

class OrdenCreate(BaseModel):
    nombre_cliente: str
    email_cliente: EmailStr
    total: Decimal

class OrdenResponse(BaseModel):
    id: int
    codigo_orden: str
    nombre_cliente: str | None
    email_cliente: str | None
    total: Decimal
    estado: str

    class Config:
        from_attributes = True
