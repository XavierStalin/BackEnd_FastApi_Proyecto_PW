from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base
from datetime import datetime

class HistorialCorreo(Base):
    __tablename__ = "historial_correos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    remitente = Column(String)      # Quién envía (remitente lógico)
    destinatario = Column(String)   # Quién recibe
    asunto = Column(String)
    contenido = Column(Text)
    fecha_envio = Column(DateTime, default=datetime.now)
    estado = Column(String)
