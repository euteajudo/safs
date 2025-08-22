from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Schema base para usuário"""
    unidade: str = Field(..., min_length=1, max_length=60, description="Unidade do usuário")
    nome: str = Field(..., min_length=1, max_length=100, description="Nome completo do usuário")
    username: str = Field(..., min_length=3, max_length=50, description="Nome de usuário único")
    email: EmailStr = Field(..., description="Email do usuário")
    foto_url: Optional[str] = Field(None, max_length=500, description="URL da foto do usuário")
    is_active: bool = Field(True, description="Se o usuário está ativo")
    is_superuser: bool = Field(False, description="Se o usuário é superusuário")
    is_chefe_unidade: bool = Field(False, description="Se o usuário é chefe de unidade")
    is_chefe_setor: bool = Field(False, description="Se o usuário é chefe de setor")
    is_funcionario: bool = Field(False, description="Se o usuário é funcionário")
    
    @validator('nome')
    def validate_nome(cls, v):
        if v and not v.strip():
            raise ValueError('Nome não pode estar vazio')
        return v.strip() if v else v
    
    @validator('username')
    def validate_username(cls, v):
        if v and not v.strip():
            raise ValueError('Username não pode estar vazio')
        # Only alphanumeric and underscore allowed
        if not v.replace('_', '').replace('.', '').isalnum():
            raise ValueError('Username deve conter apenas letras, números, underscore e ponto')
        return v.strip().lower() if v else v

class UserCreate(UserBase):
    """Schema para criação de usuário"""
    senha: str = Field(..., min_length=6, max_length=100, description="Senha do usuário (mínimo 6 caracteres)")
    
    @validator('senha')
    def validate_senha(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres')
        return v

class UserUpdate(BaseModel):
    """Schema para atualização de usuário"""
    email: Optional[str] = None
    username: Optional[str] = None
    nome: Optional[str] = None
    foto_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_chefe_unidade: Optional[bool] = None
    is_chefe_setor: Optional[bool] = None
    is_funcionario: Optional[bool] = None

class UserInDB(UserBase):
    """Schema para usuário no banco de dados"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserInDB):
    """Schema para resposta da API (sem senha)"""
    pass

# Schema interno para criação com campos automáticos
class UserCreateInternal(BaseModel):
    """Schema interno para criação de usuário com todos os campos"""
    nome: str
    username: str
    email: str
    senha: str
    foto_url: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    is_chefe_unidade: bool = False
    is_chefe_setor: bool = False
    is_funcionario: bool = False 