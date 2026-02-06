from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi_mail import ConnectionConfig
from typing import List

from database import SessionLocal, engine, Base
from config import get_settings, Settings
import models, schemas, service

# Crear las tablas en la BD
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Notificaciones")
#Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes temporalmente para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 
# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuración de correo (usando variables de entorno)
def get_mail_config(settings: Settings = Depends(get_settings)):
    return ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True
    )

# --- ENDPOINTS DE CORREO ---

@app.post("/email/", response_model=schemas.EmailResponse)
async def enviar_correo(
    email_data: schemas.EmailRequest, 
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings)
):
    mail_conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True
    )
    srv = service.EmailService(db, mail_conf)
    return await srv.send_and_save(email_data)

@app.get("/email/historial", response_model=List[schemas.EmailResponse])
def ver_historial_correos(db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    mail_conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True
    )
    srv = service.EmailService(db, mail_conf)
    return srv.get_history()