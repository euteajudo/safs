"""Schemas para token e dados de autenticação"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserInToken(BaseModel):
    """Schema para dados básicos do usuário no token"""
    id: int
    username: str
    nome: str
    email: str
    unidade: str
    is_active: bool
    is_superuser: bool
    is_chefe_unidade: bool
    is_chefe_setor: bool
    is_funcionario: bool
    foto_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class Token(BaseModel):
    """Schema para resposta de token de acesso"""
    access_token: str
    token_type: str
    user: UserInToken

class TokenData(BaseModel):
    """Schema para dados contidos no token"""
    username: Optional[str] = None