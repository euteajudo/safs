"""
Modelos de usuário para o sistema de dashboard.
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime
from datetime import datetime, timezone

from app_catalogo.models.base import Base

class User(Base):
    """
    Modelo que cria a tabela de usuários no banco de dados.
    """
    __tablename__ = "users_safs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unidade: Mapped[str] = mapped_column(String(60), nullable=False)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    foto_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_chefe_unidade: Mapped[bool] = mapped_column(Boolean, default=False)
    is_chefe_setor: Mapped[bool] = mapped_column(Boolean, default=False)
    is_funcionario: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    # RELACIONAMENTOS N:N (nova funcionalidade)
    # Relacionamentos many-to-many com itens do catálogo
    itens_comprados_nn = relationship(
        "ItensCatalogo", 
        secondary="comprador_item", 
        back_populates="compradores",
        lazy="selectin"
    )
    itens_controlados_nn = relationship(
        "ItensCatalogo", 
        secondary="controlador_item", 
        back_populates="controladores",
        lazy="selectin"
    )
    # Relacionamento many-to-many com processos
    processos_comprados = relationship(
        "PlanejamentoAquisicao", 
        secondary="comprador_processo", 
        back_populates="compradores",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, nome={self.nome!r}, email={self.email!r})"
