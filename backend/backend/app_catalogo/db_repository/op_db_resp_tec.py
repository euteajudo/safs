"""Funções de operação com o banco de dados para gerenciamento de responsáveis técnicos"""

import logging
from typing import Any, List, Optional, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app_catalogo.models.resp_tec import ResponsavelTecnico
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

logger = logging.getLogger("db_repository")


class ResponsavelTecnicoRepository:
    """Repository class for responsavel tecnico operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def criar_responsavel_tecnico(self, resp_tec_data: dict) -> ResponsavelTecnico:
        """Creates a new responsavel tecnico safely."""
        return await criar_responsavel_tecnico(self.db, resp_tec_data)
    
    async def listar_responsaveis_tecnicos_paginados(self, skip: int = 0, limit: int = 100) -> List[ResponsavelTecnico]:
        """Returns a paginated list of responsaveis tecnicos."""
        return await listar_responsaveis_tecnicos_paginados(self.db, skip, limit)
    
    async def pesquisar_responsavel_tecnico_por_id(self, resp_tec_id: int) -> Optional[ResponsavelTecnico]:
        """Searches for a responsavel tecnico by ID."""
        return await pesquisar_responsavel_tecnico_por_id(self.db, resp_tec_id)
    
    async def atualizar_responsavel_tecnico(self, resp_tec_id: int, updates: Dict[str, Any]) -> Optional[ResponsavelTecnico]:
        """Updates a responsavel tecnico by ID."""
        return await atualizar_responsavel_tecnico(self.db, resp_tec_id, updates)
    
    async def deletar_responsavel_tecnico(self, resp_tec_id: int) -> bool:
        """Deletes a responsavel tecnico by ID."""
        return await deletar_responsavel_tecnico(self.db, resp_tec_id)
    
    async def pesquisar_responsavel_tecnico_por_nome(self, nome: str) -> Optional[ResponsavelTecnico]:
        """Searches for a responsavel tecnico by name."""
        return await pesquisar_responsavel_tecnico_por_nome(self.db, nome)


async def criar_responsavel_tecnico(db: AsyncSession, resp_tec_data: dict) -> ResponsavelTecnico:
    """Insere um novo responsável técnico no banco de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        resp_tec_data (dict): Dados do responsável técnico.
    Returns:
        ResponsavelTecnico: Responsável técnico criado.
    Raises:
        IntegrityError: Se o responsável técnico já existir.
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Tentando inserir responsável técnico: {resp_tec_data.get('nome_res_tec', 'sem nome')}")
    
    responsavel_tecnico = ResponsavelTecnico(**resp_tec_data)
    try:
        db.add(responsavel_tecnico)
        await db.commit()
        await db.refresh(responsavel_tecnico)
        logger.info(f"Responsável técnico criado com sucesso. ID: {responsavel_tecnico.id}")
        return responsavel_tecnico
    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao criar responsável técnico: {e}")
        await db.rollback()
        raise e
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao criar responsável técnico: {e}", exc_info=True)
        await db.rollback()
        raise e


async def listar_responsaveis_tecnicos_paginados(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[ResponsavelTecnico]:
    """Lista responsáveis técnicos de forma paginada.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        skip (int): Número de registros para pular.
        limit (int): Número máximo de registros para retornar.
    Returns:
        List[ResponsavelTecnico]: Lista de responsáveis técnicos.
    """
    logger.info(f"Listando responsáveis técnicos paginados: skip={skip}, limit={limit}")
    
    try:
        stmt = select(ResponsavelTecnico).offset(skip).limit(limit).order_by(ResponsavelTecnico.nome_res_tec)
        result = await db.execute(stmt)
        responsaveis_tecnicos = result.scalars().all()
        logger.info(f"Responsáveis técnicos listados com sucesso: {len(responsaveis_tecnicos)} registros")
        return responsaveis_tecnicos
    except SQLAlchemyError as e:
        logger.error(f"Erro ao listar responsáveis técnicos: {e}", exc_info=True)
        raise e


async def pesquisar_responsavel_tecnico_por_id(db: AsyncSession, resp_tec_id: int) -> Optional[ResponsavelTecnico]:
    """Pesquisa um responsável técnico por ID.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        resp_tec_id (int): ID do responsável técnico.
    Returns:
        Optional[ResponsavelTecnico]: Responsável técnico encontrado ou None.
    """
    logger.info(f"Pesquisando responsável técnico por ID: {resp_tec_id}")
    
    try:
        stmt = select(ResponsavelTecnico).where(ResponsavelTecnico.id == resp_tec_id)
        result = await db.execute(stmt)
        responsavel_tecnico = result.scalar_one_or_none()
        if responsavel_tecnico:
            logger.info(f"Responsável técnico encontrado: {responsavel_tecnico.nome_res_tec}")
        else:
            logger.info(f"Responsável técnico não encontrado para ID: {resp_tec_id}")
        return responsavel_tecnico
    except SQLAlchemyError as e:
        logger.error(f"Erro ao pesquisar responsável técnico por ID: {e}", exc_info=True)
        raise e


async def atualizar_responsavel_tecnico(db: AsyncSession, resp_tec_id: int, updates: Dict[str, Any]) -> Optional[ResponsavelTecnico]:
    """Atualiza um responsável técnico por ID.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        resp_tec_id (int): ID do responsável técnico.
        updates (Dict[str, Any]): Campos para atualizar.
    Returns:
        Optional[ResponsavelTecnico]: Responsável técnico atualizado ou None se não encontrado.
    """
    logger.info(f"Atualizando responsável técnico ID {resp_tec_id} com dados: {updates}")
    
    try:
        # Buscar o responsável técnico
        stmt = select(ResponsavelTecnico).where(ResponsavelTecnico.id == resp_tec_id)
        result = await db.execute(stmt)
        responsavel_tecnico = result.scalar_one_or_none()
        
        if not responsavel_tecnico:
            logger.warning(f"Responsável técnico não encontrado para atualização: ID {resp_tec_id}")
            return None
        
        # Atualizar campos
        for field, value in updates.items():
            if hasattr(responsavel_tecnico, field) and value is not None:
                setattr(responsavel_tecnico, field, value)
        
        await db.commit()
        await db.refresh(responsavel_tecnico)
        logger.info(f"Responsável técnico ID {resp_tec_id} atualizado com sucesso")
        return responsavel_tecnico
        
    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao atualizar responsável técnico: {e}")
        await db.rollback()
        raise e
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao atualizar responsável técnico: {e}", exc_info=True)
        await db.rollback()
        raise e


async def deletar_responsavel_tecnico(db: AsyncSession, resp_tec_id: int) -> bool:
    """Deleta um responsável técnico por ID.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        resp_tec_id (int): ID do responsável técnico.
    Returns:
        bool: True se deletado com sucesso, False se não encontrado.
    """
    logger.info(f"Tentando deletar responsável técnico ID: {resp_tec_id}")
    
    try:
        # Buscar o responsável técnico
        stmt = select(ResponsavelTecnico).where(ResponsavelTecnico.id == resp_tec_id)
        result = await db.execute(stmt)
        responsavel_tecnico = result.scalar_one_or_none()
        
        if not responsavel_tecnico:
            logger.warning(f"Responsável técnico não encontrado para deleção: ID {resp_tec_id}")
            return False
        
        await db.delete(responsavel_tecnico)
        await db.commit()
        logger.info(f"Responsável técnico ID {resp_tec_id} deletado com sucesso")
        return True
        
    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao deletar responsável técnico (pode ter itens associados): {e}")
        await db.rollback()
        raise e
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao deletar responsável técnico: {e}", exc_info=True)
        await db.rollback()
        raise e


async def pesquisar_responsavel_tecnico_por_nome(db: AsyncSession, nome: str) -> Optional[ResponsavelTecnico]:
    """Pesquisa um responsável técnico por nome (busca exata).
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        nome (str): Nome do responsável técnico.
    Returns:
        Optional[ResponsavelTecnico]: Responsável técnico encontrado ou None.
    """
    logger.info(f"Pesquisando responsável técnico por nome: {nome}")
    
    try:
        stmt = select(ResponsavelTecnico).where(ResponsavelTecnico.nome_res_tec == nome)
        result = await db.execute(stmt)
        responsavel_tecnico = result.scalar_one_or_none()
        if responsavel_tecnico:
            logger.info(f"Responsável técnico encontrado: ID {responsavel_tecnico.id}")
        else:
            logger.info(f"Responsável técnico não encontrado para nome: {nome}")
        return responsavel_tecnico
    except SQLAlchemyError as e:
        logger.error(f"Erro ao pesquisar responsável técnico por nome: {e}", exc_info=True)
        raise e