from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import requests
import models, schemas
from repository import EmailRepository

class EmailService:
    def __init__(self, db: Session, mail_config: ConnectionConfig):
        self.repo = EmailRepository(db)
        self.mail_config = mail_config
        self.fast_mail = FastMail(mail_config)

    async def send_and_save(self, email_req: schemas.EmailRequest):
        estado_envio = "Pendiente"
        
        try:
            # El correo REAL se envía desde el correo del sistema
            # Pero incluimos quién es el remitente LÓGICO en el cuerpo
            cuerpo_con_remitente = f"""
            <html>
            <body>
                <p><strong>📧 Este mensaje es de: {email_req.remitente}</strong></p>
                <hr>
                <p>{email_req.cuerpo}</p>
            </body>
            </html>
            """
            
            message = MessageSchema(
                subject=f"[De: {email_req.remitente}] {email_req.asunto}",
                recipients=[email_req.destinatario],
                body=cuerpo_con_remitente,
                subtype="html"
            )
            
            await self.fast_mail.send_message(message)
            estado_envio = "Enviado"
            
        except Exception as e:
            print(f"Error enviando correo: {e}")
            estado_envio = "Fallido"

        # Guardar en BD
        nuevo_correo = models.HistorialCorreo(
            remitente=email_req.remitente,
            destinatario=email_req.destinatario,
            asunto=email_req.asunto,
            contenido=email_req.cuerpo,
            estado=estado_envio
        )
        return self.repo.save(nuevo_correo)

    def get_history(self):
        return self.repo.get_all()