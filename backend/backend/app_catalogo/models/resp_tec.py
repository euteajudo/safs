"""Modelo para Responsável Técnico"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from app_catalogo.models.base import Base


class ResponsavelTecnico(Base):
    """Modelo para a tabela de responsáveis técnicos"""
    __tablename__ = "responsaveis_tecnicos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_res_tec: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"ResponsavelTecnico(id={self.id}, nome_res_tec={self.nome_res_tec!r})"