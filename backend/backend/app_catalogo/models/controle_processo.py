"""Controle de processos"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app_catalogo.models.base import Base

class PlanejamentoAquisicao(Base):
    """Modelo que cria a tabela para controle de processos de aquisição"""
    __tablename__ = "planejamento_aquisicao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    objeto_aquisicao: Mapped[str] = mapped_column(String(255), nullable=False)
    numero_processo_planejamento: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    numero_item: Mapped[str] = mapped_column(String(10), nullable=False)
    codigo_master: Mapped[str] = mapped_column(String(20), nullable=False)
    status_processo_planejamento: Mapped[str] = mapped_column(String(50), nullable=False)
    numero_processo_compra_centralizada: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    status_compra_centralizada: Mapped[str] = mapped_column(String(50), nullable=True)
    observacao: Mapped[str] = mapped_column(String(255), nullable=True)


    def __repr__(self) -> str:
        return (
            f"PlanejamentoAquisicao(objeto_aquisicao={self.objeto_aquisicao!r}, "
            f"numero_item={self.numero_item!r}, "
            f"numero_processo_planejamento={self.numero_processo_planejamento!r})"
        )
