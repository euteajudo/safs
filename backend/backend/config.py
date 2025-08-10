from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Configurações do Banco de Dados
    database_url: str = "sqlite:///./dashboard.db"
    
    # Configurações da API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # Configurações de Segurança
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configurações CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instância global das configurações
settings = Settings() 