
from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

class StatusProcessoPlanejamento(str, Enum):
    EM_ANDAMENTO = "Em andamento"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"
    PENDENTE = "Pendente"

class StatusCompra(str, Enum):
    NAO_INICIADA = "Não iniciada"
    EM_ANDAMENTO = "Em andamento"
    FINALIZADA = "Finalizada"
    CANCELADA = "Cancelada"

class ProcessoBase(BaseModel):
    objeto_aquisicao: str = Field(..., min_length=1, max_length=500, description="Objeto da aquisição")
    numero_processo_planejamento: str = Field(..., min_length=1, max_length=50, description="Número do processo de planejamento")
    numero_item: str = Field(..., min_length=1, max_length=20, description="Número do item")
    codigo_master: str = Field(..., min_length=1, max_length=50, description="Código master do item")
    status_processo_planejamento: StatusProcessoPlanejamento = Field(..., description="Status do processo de planejamento")
    numero_processo_compra_centralizada: Optional[str] = Field(None, max_length=50, description="Número do processo de compra centralizada")
    status_compra_centralizada: Optional[StatusCompra] = Field(None, description="Status da compra centralizada")
    observacao: Optional[str] = Field(None, max_length=1000, description="Observações")
    
    @validator('objeto_aquisicao')
    def validate_objeto_aquisicao(cls, v):
        if v and not v.strip():
            raise ValueError('Objeto da aquisição não pode estar vazio')
        return v.strip() if v else v
    
    @validator('numero_processo_planejamento')
    def validate_numero_processo(cls, v):
        if v and not v.strip():
            raise ValueError('Número do processo não pode estar vazio')
        return v.strip() if v else v
    
    @validator('codigo_master')
    def validate_codigo_master(cls, v):
        if v and not v.strip():
            raise ValueError('Código master não pode estar vazio')
        return v.strip() if v else v

class ProcessoCreate(ProcessoBase):
    pass

class ProcessoUpdate(BaseModel):
    objeto_aquisicao: Optional[str] = Field(None, min_length=1, max_length=500, description="Objeto da aquisição")
    numero_processo_planejamento: Optional[str] = Field(None, min_length=1, max_length=50, description="Número do processo de planejamento")
    numero_item: Optional[str] = Field(None, min_length=1, max_length=20, description="Número do item")
    codigo_master: Optional[str] = Field(None, min_length=1, max_length=50, description="Código master do item")
    status_processo_planejamento: Optional[StatusProcessoPlanejamento] = Field(None, description="Status do processo de planejamento")
    numero_processo_compra_centralizada: Optional[str] = Field(None, max_length=50, description="Número do processo de compra centralizada")
    status_compra_centralizada: Optional[StatusCompra] = Field(None, description="Status da compra centralizada")
    observacao: Optional[str] = Field(None, max_length=1000, description="Observações")

class ProcessoRead(ProcessoBase):
    id: int

    class Config:
        from_attributes = True