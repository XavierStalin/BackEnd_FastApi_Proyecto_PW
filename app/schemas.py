from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# --- CORREO ---
class EmailRequest(BaseModel):
    remitente: EmailStr       # Correo de quien "envía" (solo informativo)
    destinatario: EmailStr    # A quién llegará el correo
    asunto: str
    cuerpo: str

class EmailResponse(BaseModel):
    id: int
    remitente: str
    destinatario: str
    asunto: str
    contenido: str
    fecha_envio: datetime
    estado: str
    
    class Config:
        from_attributes = True