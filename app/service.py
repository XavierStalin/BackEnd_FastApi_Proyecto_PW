import resend
from sqlalchemy.orm import Session
import models, schemas
from repository import EmailRepository
from config import Settings

class EmailService:
    def __init__(self, db: Session, settings: Settings):
        self.repo = EmailRepository(db)
        self.settings = settings
        resend.api_key = settings.RESEND_API_KEY

    async def send_and_save(self, email_req: schemas.EmailRequest):
        estado_envio = "Pendiente"
        
        try:
            # El correo REAL se envía desde el correo verificado en Resend (ej: onboarding@resend.dev)
            # El remitente original se menciona en el cuerpo y reply-to
            
            cuerpo_con_remitente = f"""
            <html>
            <body>
                <p><strong>📧 Mensaje de: {email_req.remitente}</strong></p>
                <hr>
                <div style="font-family: sans-serif; padding: 20px; color: #333;">
                    {email_req.cuerpo}
                </div>
            </body>
            </html>
            """
            
            params = {
                "from": self.settings.MAIL_FROM,
                "to": [email_req.destinatario],
                "subject": f"[De: {email_req.remitente}] {email_req.asunto}",
                "html": cuerpo_con_remitente,
                "reply_to": email_req.remitente
            }
            
            r = resend.Emails.send(params)
            print(f"Resend Response: {r}")
            estado_envio = "Enviado"
            
        except Exception as e:
            print(f"Error enviando correo con Resend: {e}")
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