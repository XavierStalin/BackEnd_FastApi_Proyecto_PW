from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Correo del sistema
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()