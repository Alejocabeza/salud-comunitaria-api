import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings 

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./database.db"

    APP_TITLE: str = "Salud Comunitaria API"
    APP_DESCRIPTION: str = "Aplicación de gestión de salud comunitaria"
    APP_VERSION: str = "1.0.0"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()