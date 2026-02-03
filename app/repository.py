from sqlalchemy.orm import Session
import models

class PersonaRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(models.Persona).all()

    def find_by_cedula(self, cedula: str):
        return self.db.query(models.Persona).filter(models.Persona.cedula == cedula).first()

    def save(self, persona: models.Persona):
        self.db.add(persona)
        self.db.commit()
        self.db.refresh(persona)
        return persona
    
    # Método extra por si acaso
    def delete(self, persona: models.Persona):
        self.db.delete(persona)
        self.db.commit()
        return persona
    
class CosaRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, cosa: models.Cosa):
        self.db.add(cosa)
        self.db.commit()
        self.db.refresh(cosa)
        return cosa
    
    def find_all(self):
        return self.db.query(models.Cosa).all()

    def find_by_id(self, id: int):
        return self.db.query(models.Cosa).filter(models.Cosa.id == id).first()
    
    def delete(self, cosa: models.Cosa):
        self.db.delete(cosa)
        self.db.commit()
        return cosa