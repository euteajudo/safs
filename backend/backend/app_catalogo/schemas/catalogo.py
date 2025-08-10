"""Schema de itens do catálogo"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List

from .user import User as UserRead
from .controle_processos import ProcessoRead


class ItemCatalogoBase(BaseModel):
    unidade: str = Field(..., min_length=1, max_length=20, description="Unidade organizacional")
    marca: Optional[str] = Field(None, max_length=60, description="Marca do item")
    embalagem: Optional[str] = Field(None, max_length=60, description="Embalagem do item")
    codigo_master: str = Field(..., min_length=1, max_length=50, description="Código master único do item")
    descricao: str = Field(..., min_length=1, max_length=500, description="Descrição do item")
    codigo_aghu_hu: Optional[str] = Field(None, max_length=50, description="Código AGHU HU")
    codigo_aghu_meac: Optional[str] = Field(None, max_length=50, description="Código AGHU MEAC")
    catmat: Optional[str] = Field(None, max_length=50, description="Código CATMAT")
    codigo_ebserh: Optional[str] = Field(None, max_length=50, description="Código EBSERH")
    apresentacao: Optional[str] = Field(None, max_length=200, description="Apresentação do item")
    classificacao_xyz: Optional[str] = Field(None, max_length=10, description="Classificação XYZ")
    observacao: Optional[str] = Field(None, max_length=1000, description="Observações")
    comprador_id: Optional[int] = Field(None, gt=0, description="ID do comprador")
    controlador_id: Optional[int] = Field(None, gt=0, description="ID do controlador")
    # Campo tradicional (para compatibilidade com rotas existentes)
    processo_id: Optional[int] = Field(None, gt=0, description="ID do processo principal")
    # Campo adicional para múltiplos processos
    processo_ids_adicionais: Optional[List[int]] = Field(default=[], description="IDs dos processos adicionais")
    
    @validator('codigo_master')
    def validate_codigo_master(cls, v):
        if v and not v.strip():
            raise ValueError('Código master não pode estar vazio')
        return v.strip() if v else v
    
    @validator('descricao')
    def validate_descricao(cls, v):
        if v and not v.strip():
            raise ValueError('Descrição não pode estar vazia')
        return v.strip() if v else v

class ItemCatalogoCreate(ItemCatalogoBase):
    pass

class ItemCatalogoUpdate(BaseModel):
    unidade: Optional[str] = None
    marca: Optional[str] = None
    embalagem: Optional[str] = None
    codigo_master: Optional[str] = None
    descricao: Optional[str] = None
    codigo_aghu_hu: Optional[str] = None
    codigo_aghu_meac: Optional[str] = None
    catmat: Optional[str] = None
    codigo_ebserh: Optional[str] = None
    apresentacao: Optional[str] = None
    classificacao_xyz: Optional[str] = None
    observacao: Optional[str] = None
    comprador_id: Optional[int] = None
    controlador_id: Optional[int] = None
    # Campo tradicional mantido
    processo_id: Optional[int] = None
    # Campo adicional para múltiplos processos
    processo_ids_adicionais: Optional[List[int]] = None

class ItemCatalogoRead(ItemCatalogoBase):
    id: int
    
    comprador: Optional[UserRead] = None
    controlador: Optional[UserRead] = None
    # Relacionamento tradicional mantido
    processo: Optional[ProcessoRead] = None
    # Relacionamentos adicionais
    processos_adicionais: Optional[List[ProcessoRead]] = []

    class Config:
        from_attributes = True