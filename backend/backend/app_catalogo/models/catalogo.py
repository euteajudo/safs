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

# Tabelas associativas para relacionamentos many-to-many com usuários
comprador_item_association = Table(
    'comprador_item',
    Base.metadata,
    Column('comprador_id', Integer, ForeignKey('users_safs.id', name='fk_comprador_item_user_id'), primary_key=True),
    Column('item_id', Integer, ForeignKey('itens_catalogo.id', name='fk_comprador_item_item_id'), primary_key=True)
)

controlador_item_association = Table(
    'controlador_item', 
    Base.metadata,
    Column('controlador_id', Integer, ForeignKey('users_safs.id', name='fk_controlador_item_user_id'), primary_key=True),
    Column('item_id', Integer, ForeignKey('itens_catalogo.id', name='fk_controlador_item_item_id'), primary_key=True)
)



class ItensCatalogo(Base):
    """Modelo que cria a tabela de catalogo de itens da ULOG e UACE"""
    __tablename__ = "itens_catalogo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    unidade: Mapped[str] = mapped_column(String(20), nullable=False)
    descritivo_detalhado: Mapped[str] = mapped_column(String(4000), nullable=True)
    codigo_master: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    codigo_aghu_hu: Mapped[str] = mapped_column(String(20), nullable=True)
    codigo_aghu_meac: Mapped[str] = mapped_column(String(20), nullable=True)
    catmat: Mapped[str] = mapped_column(String(20), nullable=True)
    codigo_ebserh: Mapped[str] = mapped_column(String(20), nullable=True)
    descritivo_resumido: Mapped[str] = mapped_column(String(300), nullable=False) # para aumentar a quantidade de caracteres, basta aumentar o valor do campo
    apresentacao: Mapped[str] = mapped_column(String(100), nullable=True)
    classificacao_xyz: Mapped[str] = mapped_column(String(10), nullable=True)


    comprador_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_safs.id"), nullable=True)
    controlador_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_safs.id"), nullable=True)
    responsavel_tecnico_id: Mapped[int] = mapped_column(Integer, ForeignKey("responsaveis_tecnicos.id"), nullable=True)

    # RELACIONAMENTOS 1:N (mantidos para compatibilidade)
    comprador = relationship("User", foreign_keys=[comprador_id], backref="itens_comprados")
    controlador = relationship("User", foreign_keys=[controlador_id], backref="itens_controlados")
    responsavel_tecnico = relationship("ResponsavelTecnico", foreign_keys=[responsavel_tecnico_id], backref="itens_catalogo")
    
    # RELACIONAMENTOS N:N (nova funcionalidade)
    # Relacionamento many-to-many com processos
    processos_adicionais = relationship(
        "PlanejamentoAquisicao", 
        secondary=item_processo_association, 
        backref="itens_catalogo_adicionais",
        lazy="selectin"
    )
    # Relacionamentos many-to-many com usuários
    compradores = relationship(
        "User", 
        secondary=comprador_item_association, 
        back_populates="itens_comprados_nn",
        lazy="selectin"
    )
    controladores = relationship(
        "User", 
        secondary=controlador_item_association, 
        back_populates="itens_controlados_nn",
        lazy="selectin"
    )

    observacao: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"ItensCatalogo(id={self.id})"


