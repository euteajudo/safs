"""Schemas para token e dados de autenticação"""
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Schema para resposta de token de acesso"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema para dados contidos no token"""
    username: Optional[str] = None