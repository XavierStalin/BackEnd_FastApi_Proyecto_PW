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
    cosas = relationship("Cosa", back_populates="propietario")

class Cosa(Base):
    __tablename__ = "cosas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descripcion = Column(String)
    monto = Column(Float)

    # La llave foránea siempre va en el lado de "Muchos" (La Cosa tiene el dueño)
    persona_cedula = Column(String, ForeignKey("personas.cedula"))
    
    # Lado "Muchos":
    # back_populates debe decir "cosas" porque así se llama la variable en Persona
    propietario = relationship("Persona", back_populates="cosas")
    #En caso de querer hacer una relación simple sin back_populates:
    #El ForeignKey es obligatorio
    #persona_cedula = Column(String, ForeignKey("personas.cedula"))
    # CAMBIO: Quitas back_populates. Ahora es una relación simple.
    #propietario = relationship("Persona")