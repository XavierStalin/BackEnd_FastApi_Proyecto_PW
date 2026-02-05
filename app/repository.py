from sqlalchemy.orm import Session
import models


class EmailRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, correo_data: models.HistorialCorreo):
        """Guarda un nuevo registro de correo en la base de datos"""
        self.db.add(correo_data)
        self.db.commit()
        self.db.refresh(correo_data)
        return correo_data

    def get_all(self):
        """Obtiene todos los registros de correos"""
        return self.db.query(models.HistorialCorreo).all()

    def get_by_id(self, correo_id: int):
        """Obtiene un correo específico por ID"""
        return self.db.query(models.HistorialCorreo).filter(
            models.HistorialCorreo.id == correo_id
        ).first()

    def get_by_remitente(self, remitente: str):
        """Obtiene todos los correos de un remitente específico"""
        return self.db.query(models.HistorialCorreo).filter(
            models.HistorialCorreo.remitente == remitente
        ).all()
