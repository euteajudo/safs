"""Schema de itens do catálogo"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List

from .user import User as UserRead
from .controle_processos import ProcessoRead


class ItemCatalogoBase(BaseModel):
    unidade: str = Field(..., min_length=1, max_length=20, description="Unidade organizacional")
    descritivo_detalhado: Optional[str] = Field(None, max_length=4000, description="Descritivo detalhado do item")
    codigo_master: str = Field(..., min_length=1, max_length=20, description="Código master único do item")
    descritivo_resumido: str = Field(..., min_length=1, max_length=300, description="Descritivo resumido do item")
    codigo_aghu_hu: Optional[str] = Field(None, max_length=20, description="Código AGHU HU")
    codigo_aghu_meac: Optional[str] = Field(None, max_length=20, description="Código AGHU MEAC")
    catmat: Optional[str] = Field(None, max_length=20, description="Código CATMAT")
    codigo_ebserh: Optional[str] = Field(None, max_length=20, description="Código EBSERH")
    apresentacao: Optional[str] = Field(None, max_length=100, description="Apresentação do item")
    classificacao_xyz: Optional[str] = Field(None, max_length=10, description="Classificação XYZ")
    responsavel_tecnico: Optional[str] = Field(None, max_length=100, description="Responsável técnico")
    observacao: Optional[str] = Field(None, max_length=255, description="Observações")
    # CAMPOS 1:N (mantidos para compatibilidade)
    comprador_id: Optional[int] = Field(None, description="ID do comprador")
    controlador_id: Optional[int] = Field(None, description="ID do controlador")
    
    # CAMPOS N:N (nova funcionalidade)
    # Campo para múltiplos processos (sem processo principal)
    processo_ids: Optional[List[int]] = Field(default=[], description="IDs dos processos de aquisição")
    # Campos para múltiplos usuários
    comprador_ids: Optional[List[int]] = Field(default=[], description="IDs dos compradores")
    controlador_ids: Optional[List[int]] = Field(default=[], description="IDs dos controladores")
    responsavel_tecnico_ids: Optional[List[int]] = Field(default=[], description="IDs dos responsáveis técnicos")
    
    @validator('codigo_master')
    def validate_codigo_master(cls, v):
        if v and not v.strip():
            raise ValueError('Código master não pode estar vazio')
        return v.strip() if v else v
    
    @validator('descritivo_resumido')
    def validate_descritivo_resumido(cls, v):
        if v and not v.strip():
            raise ValueError('Descritivo resumido não pode estar vazio')
        return v.strip() if v else v

class ItemCatalogoCreate(ItemCatalogoBase):
    pass

class ItemCatalogoUpdate(BaseModel):
    unidade: Optional[str] = None
    descritivo_detalhado: Optional[str] = None
    codigo_master: Optional[str] = None
    descritivo_resumido: Optional[str] = None
    codigo_aghu_hu: Optional[str] = None
    codigo_aghu_meac: Optional[str] = None
    catmat: Optional[str] = None
    codigo_ebserh: Optional[str] = None
    apresentacao: Optional[str] = None
    classificacao_xyz: Optional[str] = None
    responsavel_tecnico: Optional[str] = None
    observacao: Optional[str] = None
    # CAMPOS 1:N (mantidos para compatibilidade)
    comprador_id: Optional[int] = None
    controlador_id: Optional[int] = None
    responsavel_tecnico_id: Optional[int] = None
    
    # CAMPOS N:N (nova funcionalidade)
    # Campo para múltiplos processos
    processo_ids: Optional[List[int]] = None
    # Campos para múltiplos usuários
    comprador_ids: Optional[List[int]] = None
    controlador_ids: Optional[List[int]] = None
    responsavel_tecnico_ids: Optional[List[int]] = None

class ItemCatalogoRead(ItemCatalogoBase):
    id: int
    
    # RELACIONAMENTOS 1:N (mantidos para compatibilidade)
    comprador: Optional[UserRead] = None
    controlador: Optional[UserRead] = None
    
    # RELACIONAMENTOS N:N (nova funcionalidade)
    # Relacionamentos com processos
    processos_adicionais: Optional[List[ProcessoRead]] = []
    # Relacionamentos com múltiplos usuários
    compradores: Optional[List[UserRead]] = []
    controladores: Optional[List[UserRead]] = []
    responsaveis_tecnicos: Optional[List[UserRead]] = []

    class Config:
        from_attributes = True