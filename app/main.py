from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database, service
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Persona CRUD FastAPI")

# --- AGREGA ESTO ---
origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permitir GET, POST, PUT, DELETE
    allow_headers=["*"],
)

# Crea las tablas automáticamente al iniciar
models.Base.metadata.create_all(bind=database.engine)

# Inyección de Dependencia para el Servicio
def get_persona_service(db: Session = Depends(database.get_db)):
    return service.PersonaService(db)

def get_cosa_service(db: Session = Depends(database.get_db)):
    return service.CosaService(db)

@app.get("/api/personas", response_model=List[schemas.Persona])
def read_personas(svc: service.PersonaService = Depends(get_persona_service)):
    return svc.get_all()

@app.post("/api/personas", response_model=schemas.Persona, status_code=201)
def create_persona(persona: schemas.PersonaCreate, svc: service.PersonaService = Depends(get_persona_service)):
    return svc.create(persona)

@app.get("/api/personas/{cedula}", response_model=schemas.Persona)
def read_persona(cedula: str, svc: service.PersonaService = Depends(get_persona_service)):
    persona = svc.get_by_cedula(cedula)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona
@app.put("/api/personas/{cedula}", response_model=schemas.Persona)
def update_persona(cedula: str, persona: schemas.PersonaUpdate, svc: service.PersonaService = Depends(get_persona_service)):
    updated_persona = svc.update(cedula, persona)
    
    if not updated_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada, no se puede actualizar")
    
    return updated_persona

@app.delete("/api/personas/{cedula}", status_code=204)
def delete_persona(cedula: str, svc: service.PersonaService = Depends(get_persona_service)):
    deleted_persona = svc.delete(cedula)
    
    if not deleted_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada, no se puede eliminar")
    
    return
#----------------------------------------------------------------------------
@app.post("/api/cosas", response_model=schemas.Cosa, status_code=201)
def create_cosa(cosa: schemas.CosaCreate, svc: service.CosaService = Depends(get_cosa_service)):
    nueva_cosa = svc.create(cosa)
    if not nueva_cosa:
        raise HTTPException(status_code=404, detail="Persona no encontrada, no se puede crear la cosa")
    return nueva_cosa

@app.get("/api/cosas", response_model=List[schemas.Cosa])
def read_cosas(svc: service.CosaService = Depends(get_cosa_service)):
    return svc.get_all()


@app.get("/api/cosas/{id}", response_model=schemas.Cosa)
def read_cosa_by_id(id: int, svc: service.CosaService = Depends(get_cosa_service)):
    cosa = svc.get_by_id(id)
    if not cosa:
        raise HTTPException(status_code=404, detail="Cosa not found")
    return cosa