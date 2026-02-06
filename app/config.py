from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # --- Configuración de Base de Datos ---
    # Por defecto usamos una cadena vacía o local para evitar errores si falta la variable,
    # pero en Railway esta variable SERÁ inyectada.
    DATABASE_URL: str = "postgresql://postgres:system@localhost:5432/pruebaPW"

    # --- Configuración de Correo ---
    MAIL_USERNAME: str = "tu_correo_por_defecto@gmail.com" # Valor default opcional
    MAIL_PASSWORD: str = "tu_password"
    MAIL_FROM: str = "tu_correo@gmail.com"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.gmail.com"
    
    class Config:
        # Pydantic leerá primero las variables de entorno del sistema (Railway),
        # y si no las encuentra, buscará en el archivo .env
        env_file = ".env"
        extra = "ignore" # Ignora variables extra en el .env que no estén aquí defined

@lru_cache()
def get_settings():
    return Settings()