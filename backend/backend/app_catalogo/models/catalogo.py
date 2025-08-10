from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from app_catalogo.models.base import Base

# Tabela associativa para relacionamento many-to-many entre itens e processos
item_processo_association = Table(
    'item_processo',
    Base.metadata,
    Column('item_id', Integer, ForeignKey('itens_catalogo.id', name='fk_item_processo_item_id'), primary_key=True),
    Column('processo_id', Integer, ForeignKey('planejamento_aquisicao.id', name='fk_item_processo_processo_id'), primary_key=True)
)

class ItensCatalogo(Base):
    """Modelo que cria a tabela de catalogo de itens da ULOG e UACE"""
    __tablename__ = "itens_catalogo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    unidade: Mapped[str] = mapped_column(String(20), nullable=False)
    marca: Mapped[str] = mapped_column(String(60), nullable=True)
    embalagem: Mapped[str] = mapped_column(String(60), nullable=True)
    codigo_master: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    codigo_aghu_hu: Mapped[str] = mapped_column(String(20), nullable=True)
    codigo_aghu_meac: Mapped[str] = mapped_column(String(20), nullable=True)
    catmat: Mapped[str] = mapped_column(String(20), nullable=True)
    codigo_ebserh: Mapped[str] = mapped_column(String(20), nullable=True)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    apresentacao: Mapped[str] = mapped_column(String(100), nullable=True)
    classificacao_xyz: Mapped[str] = mapped_column(String(10), nullable=True)

    comprador_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_safs.id"), nullable=True)
    controlador_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_safs.id"), nullable=True)
    # Mantido processo_id para compatibilidade com rotas existentes
    processo_id: Mapped[int] = mapped_column(Integer, ForeignKey("planejamento_aquisicao.id"), nullable=True)

    comprador = relationship("User", foreign_keys=[comprador_id], backref="itens_comprados")
    controlador = relationship("User", foreign_keys=[controlador_id], backref="itens_controlados")
    # Relacionamento tradicional (para compatibilidade)
    processo = relationship("PlanejamentoAquisicao", foreign_keys=[processo_id], backref="itens")
    # Relacionamento many-to-many com processos (funcionalidade adicional)
    processos_adicionais = relationship(
        "PlanejamentoAquisicao", 
        secondary=item_processo_association, 
        backref="itens_catalogo_adicionais",
        lazy="selectin"
    )

    observacao: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return (f"ItensCatalogo(codigo_master={self.codigo_master!r}, descricao={self.descricao!r})")


