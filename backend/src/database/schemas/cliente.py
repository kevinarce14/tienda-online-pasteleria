from pydantic import BaseModel, EmailStr
from typing import Optional


class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True
