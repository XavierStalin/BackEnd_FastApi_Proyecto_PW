from pydantic import BaseModel
from typing import Optional

class CosaBase(BaseModel):
    descripcion: str
    monto: float

class CosaCreate(CosaBase):
    persona_cedula: str

class CosaUpdate(BaseModel):
    descripcion: Optional[str] = None
    monto: Optional[float] = None
    

class Cosa(CosaBase):
    id: int
    persona_cedula: str
    class Config:
        from_attributes = True  # Vital para compatibilidad con ORM





#--------------------------------------------------------------------
class PersonaBase(BaseModel):
    cedula: str
    nombre: str
    direccion: str

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(BaseModel):
    cedula: Optional[str] = None
    nombre: Optional[str] = None
    direccion: Optional[str] = None

class Persona(PersonaBase):
    # Opcional: Si quieres ver los pedidos cuando pidas la persona
    # pedidos: List[Pedido] = []
    class Config:
        from_attributes = True  # Vital para compatibilidad con ORM