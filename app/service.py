from sqlalchemy.orm import Session
from repository import CosaRepository, PersonaRepository
import models, schemas

class PersonaService:
    def __init__(self, db: Session):
        self.repo = PersonaRepository(db)

    def get_all(self):
        return self.repo.find_all()

    def get_by_cedula(self, cedula: str):
        return self.repo.find_by_cedula(cedula)

    def create(self, persona_data: schemas.PersonaCreate):
        # Convierte el esquema (DTO) a Modelo de Base de Datos
        persona = models.Persona(**persona_data.model_dump())
        return self.repo.save(persona)
    
    def update(self, cedula: str, persona_data: schemas.PersonaUpdate):
        # 1. Buscar si existe en la base de datos
        db_persona = self.repo.find_by_cedula(cedula)
        if not db_persona:
            return None # Le avisamos al controller que no existe
        # 2. Actualizar los campos
        # exclude_unset=True significa: "Ignora los campos que el usuario no envió"
        update_data = persona_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_persona, key, value) # Actualiza el atributo del objeto
        # 3. Guardar los cambios (Reusamos el método save del repo)
        return self.repo.save(db_persona)
    
    def delete(self, cedula: str):
        # 1. Buscar si existe en la base de datos
        db_persona = self.repo.find_by_cedula(cedula)
        if not db_persona:
            return None # Le avisamos al controller que no existe
        # 2. Borrar de la base de datos
        return self.repo.delete(db_persona)
    

class CosaService:
    def __init__(self, db: Session):
        self.repo = CosaRepository(db)
        self.persona_repo = PersonaRepository(db)

    def get_all(self):
        return self.repo.find_all()

    def get_by_id(self, id: int):
        return self.repo.find_by_id(id)

    def create(self, cosa_data: schemas.CosaCreate):
        # Convierte el esquema (DTO) a Modelo de Base de Datos
        persona_existente = self.persona_repo.find_by_cedula(cosa_data.persona_cedula)
        if not persona_existente:
            return None
        cosa = models.Cosa(**cosa_data.model_dump())
        return self.repo.save(cosa)
    
    