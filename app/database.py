from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

# 1. Obtenemos la URL desde las variables de entorno
db_url = settings.DATABASE_URL

# 2. FIX: SQLAlchemy removió el soporte para "postgres://", requiere "postgresql://"
# Railway a veces usa el formato antiguo, así que lo corregimos si es necesario.
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# 3. Creamos el engine con la URL dinámica
engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()