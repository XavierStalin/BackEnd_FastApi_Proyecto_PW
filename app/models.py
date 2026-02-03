from sqlalchemy import Column, Float, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Persona(Base):
    __tablename__ = "personas"

    cedula = Column(String, primary_key=True, index=True) 
    nombre = Column(String)
    direccion = Column(String)

    # Lado "Uno": Una persona tiene muchas cosas
    # La variable se llama 'cosas', recuérdalo.
    cosas = relationship("Cosa", back_populates="propietario")#, uselist=False<--- Si es uno a uno)

#una persona tiene muchas cosas
class Cosa(Base):
    __tablename__ = "cosas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descripcion = Column(String)
    monto = Column(Float)

    # La llave foránea siempre va en el lado de "Muchos" (La Cosa tiene el dueño)
    persona_cedula = Column(String, ForeignKey("personas.cedula"))
    
    # Lado "Muchos":
    # back_populates debe decir "cosas" porque así se llama la variable en Persona
    propietario = relationship("Persona", back_populates="cosas") # persona_cedula = Column(String, ForeignKey("personas.cedula"), unique=True)<--- Si es uno a uno)
    
    
    #En caso de querer hacer una relación simple sin back_populates:
    #El ForeignKey es obligatorio
    #persona_cedula = Column(String, ForeignKey("personas.cedula"))
    # CAMBIO: Quitas back_populates. Ahora es una relación simple.
    #propietario = relationship("Persona")








"""
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

# --- 1. LA TABLA INTERMEDIA (El Puente) ---
# No es una clase, es una variable 'Table'. Solo guarda las llaves de ambos.
persona_cosa_association = Table(
    'persona_cosa', # Nombre de la tabla en la BD
    Base.metadata,
    Column('persona_cedula', String, ForeignKey('personas.cedula'), primary_key=True),
    Column('cosa_id', Integer, ForeignKey('cosas.id'), primary_key=True)
)

# --- 2. LAS CLASES ---

class Persona(Base):
    __tablename__ = "personas"

    cedula = Column(String, primary_key=True, index=True)
    nombre = Column(String)
    direccion = Column(String)

    # CAMBIO: Usamos 'secondary' para apuntar a la tabla intermedia
    cosas = relationship("Cosa", secondary=persona_cosa_association, back_populates="propietarios")

class Cosa(Base):
    __tablename__ = "cosas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descripcion = Column(String)
    monto = Column(Float)

    # CAMBIO: ¡YA NO HAY ForeignKey AQUÍ!
    # La relación se hace mágicamente a través de 'secondary'
    propietarios = relationship("Persona", secondary=persona_cosa_association, back_populates="cosas")

"""