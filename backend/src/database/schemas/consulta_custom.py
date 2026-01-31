from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class ConsultaCustomCreate(BaseModel):
    nombre: str
    email: EmailStr
    fecha_evento: date
    invitados: Optional[str] = None
    detalles: Optional[str] = None


class ConsultaCustomResponse(ConsultaCustomCreate):
    id: int
    estado: str

    class Config:
        from_attributes = True
