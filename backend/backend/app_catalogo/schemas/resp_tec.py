"""Schema para o modelo de responsáveis técnicos"""

from pydantic import BaseModel, Field, validator
from typing import Optional


class ResponsavelTecnicoBase(BaseModel):
    """Schema base para responsável técnico"""
    nome_res_tec: str = Field(..., min_length=1, max_length=255, description="Nome do responsável técnico")
    
    @validator('nome_res_tec')
    def validate_nome_res_tec(cls, v):
        if v and not v.strip():
            raise ValueError('Nome do responsável técnico não pode estar vazio')
        return v.strip() if v else v


class ResponsavelTecnicoCreate(ResponsavelTecnicoBase):
    """Schema para criação de responsável técnico"""
    pass


class ResponsavelTecnicoUpdate(BaseModel):
    """Schema para atualização de responsável técnico"""
    nome_res_tec: Optional[str] = Field(None, min_length=1, max_length=255, description="Nome do responsável técnico")
    
    @validator('nome_res_tec')
    def validate_nome_res_tec(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Nome do responsável técnico não pode estar vazio')
        return v.strip() if v else v


class ResponsavelTecnicoRead(ResponsavelTecnicoBase):
    """Schema para leitura de responsável técnico"""
    id: int
    
    class Config:
        from_attributes = True