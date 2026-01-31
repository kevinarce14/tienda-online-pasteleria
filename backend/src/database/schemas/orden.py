from pydantic import BaseModel, EmailStr
from decimal import Decimal

class OrdenCreate(BaseModel):
    nombre_cliente: str
    email_cliente: EmailStr
    total: Decimal

class OrdenResponse(OrdenCreate):
    id: int
    estado: str

    class Config:
        from_attributes = True
