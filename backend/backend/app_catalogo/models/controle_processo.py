"""Controle de processos"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from app_catalogo.models.base import Base

# Tabela associativa para relacionamento many-to-many entre compradores e processos
comprador_processo_association = Table(
    'comprador_processo',
    Base.metadata, 
    Column('comprador_id', Integer, ForeignKey('users_safs.id', name='fk_comprador_processo_user_id'), primary_key=True),
    Column('processo_id', Integer, ForeignKey('planejamento_aquisicao.id', name='fk_comprador_processo_processo_id'), primary_key=True)
)

class PlanejamentoAquisicao(Base):
    """Modelo que cria a tabela para controle de processos de aquisição"""
    __tablename__ = "planejamento_aquisicao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unidade: Mapped[str] = mapped_column(String(60), nullable=False)
    objeto_aquisicao: Mapped[str] = mapped_column(String(255), nullable=False)
    numero_processo_planejamento: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    numero_item: Mapped[str] = mapped_column(String(10), nullable=False)
    codigo_master: Mapped[str] = mapped_column(String(20), nullable=False)
    status_processo_planejamento: Mapped[str] = mapped_column(String(50), nullable=False)
    numero_processo_compra_centralizada: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    status_compra_centralizada: Mapped[str] = mapped_column(String(50), nullable=True)
    observacao: Mapped[str] = mapped_column(String(255), nullable=True)

    # RELACIONAMENTO N:N com compradores
    compradores = relationship(
        "User", 
        secondary=comprador_processo_association, 
        back_populates="processos_comprados",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return (
            f"PlanejamentoAquisicao(objeto_aquisicao={self.objeto_aquisicao!r}, "
            f"numero_item={self.numero_item!r}, "
            f"numero_processo_planejamento={self.numero_processo_planejamento!r})"
        )
