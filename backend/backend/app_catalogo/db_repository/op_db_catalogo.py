"""Funções de operação com o banco de dados para gerenciamento da tabela do catalogo"""

import logging
from typing import Any, List, Optional, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app_catalogo.models.catalogo import ItensCatalogo
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import selectinload

from app_catalogo.models.controle_processo import PlanejamentoAquisicao

logger = logging.getLogger("db_repository")


class ItemCatalogoRepository:
    """Repository class for catalog item operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def criar_item(self, item_data: dict) -> ItensCatalogo:
        """Creates a new catalog item safely."""
        return await criar_item(self.db, item_data)
    
    async def listar_itens_paginados(self, skip: int = 0, limit: int = 100) -> List[ItensCatalogo]:
        """Returns a paginated list of catalog items."""
        return await listar_itens_paginados(self.db, skip, limit)
    
    async def pesquisar_item_por_id(self, item_id: int) -> Optional[ItensCatalogo]:
        """Searches for a catalog item by ID."""
        return await pesquisar_item_por_id(self.db, item_id)
    
    async def atualizar_item(self, item_id: int, updates: Dict[str, Any]) -> Optional[ItensCatalogo]:
        """Updates a catalog item by ID."""
        return await atualizar_item(self.db, item_id, updates)
    
    async def deletar_item(self, item_id: int) -> bool:
        """Deletes a catalog item by ID."""
        return await deletar_item(self.db, item_id)
    
    async def pesquisar_item_por_codigo_master(self, codigo_master: str) -> Optional[ItensCatalogo]:
        """Searches for a catalog item by master code."""
        return await pesquisar_item_por_codigo_master(self.db, codigo_master)
    
    async def pesquisar_item_por_descricao(self, descricao: str) -> Optional[ItensCatalogo]:
        """Searches for the first catalog item by description."""
        return await pesquisar_item_por_descricao(self.db, descricao)
    
    async def listar_processos_por_codigo_master(self, codigo_master: str, skip: int = 0, limit: int = 100) -> list[PlanejamentoAquisicao]:
        """Returns all planning processes associated with the given master code."""
        return await listar_processos_por_codigo_master(self.db, codigo_master, skip, limit)
    
    async def listar_itens_por_unidade(self, unidade: str) -> List[ItensCatalogo]:
        """Returns all catalog items associated with the given unit."""
        return await listar_itens_por_unidade(self.db, unidade)



async def criar_item(db: AsyncSession, item_data: dict) -> ItensCatalogo:
    """Insere um novo item no catálogo de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        item_data (dict): Dados do item.
    Returns:
        ItensCatalogo: Item criado.
    Raises:
        IntegrityError: Se o item já existir.
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Tentando inserir item no catálogo: {item_data}")
    
    # Separar processo_ids dos outros dados (relacionamentos N:N)
    processo_ids = item_data.pop('processo_ids', [])
    comprador_ids = item_data.pop('comprador_ids', [])
    controlador_ids = item_data.pop('controlador_ids', [])
    responsavel_tecnico_ids = item_data.pop('responsavel_tecnico_ids', [])
    
    item = ItensCatalogo(**item_data)
    try:
        db.add(item)
        await db.flush()  # Para obter o ID do item antes do commit
        
        # Adicionar processos se fornecidos
        if processo_ids:
            from app_catalogo.models.controle_processo import PlanejamentoAquisicao
            processos = await db.execute(
                select(PlanejamentoAquisicao).where(PlanejamentoAquisicao.id.in_(processo_ids))
            )
            item.processos_adicionais.extend(processos.scalars().all())
            
        # Adicionar usuários nos relacionamentos N:N se fornecidos
        if comprador_ids or controlador_ids or responsavel_tecnico_ids:
            from app_catalogo.models.user import User
            
            if comprador_ids:
                compradores = await db.execute(
                    select(User).where(User.id.in_(comprador_ids))
                )
                item.compradores.extend(compradores.scalars().all())
                
            if controlador_ids:
                controladores = await db.execute(
                    select(User).where(User.id.in_(controlador_ids))
                )
                item.controladores.extend(controladores.scalars().all())
                
            if responsavel_tecnico_ids:
                responsaveis = await db.execute(
                    select(User).where(User.id.in_(responsavel_tecnico_ids))
                )
                item.responsaveis_tecnicos.extend(responsaveis.scalars().all())
        
        await db.commit()
        await db.refresh(item)
        logger.info(f"Item criado com sucesso. ID: {item.id}")
        return item
    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao criar item. Código master duplicado ou FK inválida? {e}")
        await db.rollback()
        raise e  # Re-levanta para a API decidir o que fazer (ex: 409 Conflict)
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao criar item: {e}", exc_info=True)
        await db.rollback()
        raise e




async def listar_itens_paginados(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[ItensCatalogo]:
    """Retorna uma lista paginada de itens, otimizando o carregamento de relacionamentos.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        skip (int): Número de registros a serem ignorados.
        limit (int): Número máximo de registros a serem retornados.
    Returns:
        List[ItensCatalogo]: Lista de itens.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Buscando itens do catálogo... Página(skip={skip}, limit={limit})")
    try:
        query = (
            select(ItensCatalogo)
            .options(
                selectinload(ItensCatalogo.comprador),
                selectinload(ItensCatalogo.controlador),
                selectinload(ItensCatalogo.processos_adicionais),
                selectinload(ItensCatalogo.compradores),
                selectinload(ItensCatalogo.controladores),
                selectinload(ItensCatalogo.responsaveis_tecnicos)
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao listar itens: {e}", exc_info=True)
        return []

async def pesquisar_item_por_id(db: AsyncSession, item_id: int) -> Optional[ItensCatalogo]:
    """Busca um item do catálogo pelo ID de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        item_id (int): ID do item.
    Returns:
        Optional[ItensCatalogo]: Item encontrado ou None.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Buscando item do catálogo pelo ID: {item_id}")
    try:
        return await db.get(ItensCatalogo, item_id)
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar item por ID {item_id}: {e}", exc_info=True)
        return None



async def atualizar_item(db: AsyncSession, item_id: int, updates: Dict[str, Any]) -> Optional[ItensCatalogo]:
    """Atualiza um item do catálogo pelo ID de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        item_id (int): ID do item.
        updates (Dict[str, Any]): Campos a atualizar.
    Returns:
        Optional[ItensCatalogo]: Item atualizado ou None.
    Raises:
        IntegrityError: Se o item já existir.
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    try:
        item = await db.get(ItensCatalogo, item_id)
        if not item:
            logger.warning(f"Item com ID {item_id} não encontrado para atualização.")
            return None

        # Separar campos de relacionamentos N:N dos outros updates
        processo_ids = updates.pop('processo_ids', None)
        comprador_ids = updates.pop('comprador_ids', None)
        controlador_ids = updates.pop('controlador_ids', None)
        responsavel_tecnico_ids = updates.pop('responsavel_tecnico_ids', None)
        
        # Atualizar campos normais (incluindo campos 1:N tradicionais)
        for key, value in updates.items():
            setattr(item, key, value)
        
        # Atualizar processos se fornecidos
        if processo_ids is not None:
            from app_catalogo.models.controle_processo import PlanejamentoAquisicao
            
            # Limpar processos existentes
            item.processos_adicionais.clear()
            
            # Adicionar novos processos
            if processo_ids:
                processos = await db.execute(
                    select(PlanejamentoAquisicao).where(PlanejamentoAquisicao.id.in_(processo_ids))
                )
                item.processos_adicionais.extend(processos.scalars().all())
        
        # Atualizar usuários nos relacionamentos N:N se fornecidos
        if any(ids is not None for ids in [comprador_ids, controlador_ids, responsavel_tecnico_ids]):
            from app_catalogo.models.user import User
            
            if comprador_ids is not None:
                item.compradores.clear()
                if comprador_ids:
                    compradores = await db.execute(
                        select(User).where(User.id.in_(comprador_ids))
                    )
                    item.compradores.extend(compradores.scalars().all())
                    
            if controlador_ids is not None:
                item.controladores.clear()
                if controlador_ids:
                    controladores = await db.execute(
                        select(User).where(User.id.in_(controlador_ids))
                    )
                    item.controladores.extend(controladores.scalars().all())
                    
            if responsavel_tecnico_ids is not None:
                item.responsaveis_tecnicos.clear()
                if responsavel_tecnico_ids:
                    responsaveis = await db.execute(
                        select(User).where(User.id.in_(responsavel_tecnico_ids))
                    )
                    item.responsaveis_tecnicos.extend(responsaveis.scalars().all())
        
        await db.commit()
        await db.refresh(item)
        logger.info(f"Item {item_id} atualizado com sucesso.")
        return item
    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao atualizar item {item_id}. Código master duplicado? {e}")
        await db.rollback()
        return None
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao atualizar item {item_id}: {e}", exc_info=True)
        await db.rollback()
        return None


async def deletar_item(db: AsyncSession, item_id: int) -> bool:
    """Remove um item do catálogo pelo ID de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        item_id (int): ID do item.
    Returns:
        bool: True se removido, False se não encontrado.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    try:
        item = await db.get(ItensCatalogo, item_id)
        if not item:
            logger.warning(f"Item com ID {item_id} não encontrado para remoção.")
            return False
        
        await db.delete(item)
        await db.commit()
        logger.info(f"Item {item_id} removido com sucesso.")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao remover item {item_id}: {e}", exc_info=True)
        await db.rollback()
        return False



async def pesquisar_item_por_codigo_master(db: AsyncSession, codigo_master: str) -> Optional[ItensCatalogo]:
    """Busca um item pelo código master (que é único) de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        codigo_master (str): Código master do item.
    Returns:
        Optional[ItensCatalogo]: Item encontrado ou None.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Buscando item pelo código master: {codigo_master}")
    try:
        query = select(ItensCatalogo).where(ItensCatalogo.codigo_master == codigo_master)
        result = await db.execute(query)
        # .scalar_one_or_none() é apropriado aqui pois a coluna é ÚNICA no DB.
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar item por código master {codigo_master}: {e}", exc_info=True)
        return None




async def pesquisar_item_por_descricao(db: AsyncSession, descricao: str) -> Optional[ItensCatalogo]:
    """Busca o *primeiro* item encontrado pela descrição (que não é única) de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        descricao (str): Descrição do item.
    Returns:
        Optional[ItensCatalogo]: Item encontrado ou None.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Buscando item pela descrição: {descricao}")
    try:
        query = select(ItensCatalogo).where(ItensCatalogo.descritivo_resumido == descricao)
        result = await db.execute(query)
        # .scalars().first() é a escolha segura aqui, pois a descrição NÃO é única.
        return result.scalars().first()
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar item por descrição {descricao}: {e}", exc_info=True)
        return None

async def listar_itens_por_unidade(db: AsyncSession, unidade: str) -> List[ItensCatalogo]:
    """Retorna todos os itens associados à unidade informada.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        unidade (str): Unidade organizacional.
    Returns:
        List[ItensCatalogo]: Lista de itens associados à unidade.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Buscando itens por unidade: {unidade}")
    try:
        query = select(ItensCatalogo).where(ItensCatalogo.unidade == unidade)
        result = await db.execute(query)
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar itens por unidade {unidade}: {e}", exc_info=True)
        return []

async def listar_processos_por_codigo_master(
    session: AsyncSession, 
    codigo_master: str,
    skip: int = 0,
    limit: int = 100
) -> list[PlanejamentoAquisicao]:
    """
    Retorna todos os processos de planejamento associados ao código master informado,
    de forma segura e paginada.
    Args:
        session (AsyncSession): Sessão assíncrona SQLAlchemy.
        codigo_master (str): Código master do item.
        skip (int): Número de registros a serem ignorados.
        limit (int): Número máximo de registros a serem retornados.
    Returns:
        list[PlanejamentoAquisicao]: Lista de processos de planejamento associados ao código master.
    """
    logger.info(f"Buscando processos para o código master '{codigo_master}'... Página(skip={skip}, limit={limit})")
    try:
        # --- LÓGICA CORRIGIDA ---
        query = (
            select(PlanejamentoAquisicao)
            # Filtra pela coluna correta 'codigo_master'
            .where(PlanejamentoAquisicao.codigo_master == codigo_master)
            .offset(skip)
            .limit(limit)
        )
        
        result = await session.execute(query)
        return result.scalars().all()

    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar processos para o código master '{codigo_master}': {e}", exc_info=True)
        return []


# =============================================================================
# FUNÇÕES PARA RELACIONAMENTOS MANY-TO-MANY (Nova funcionalidade)
# =============================================================================

async def associar_compradores_item(
    db: AsyncSession, 
    item_id: int, 
    comprador_ids: List[int]
) -> Optional[ItensCatalogo]:
    """
    Associa múltiplos compradores a um item do catálogo (relacionamento N:N).
    
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        item_id (int): ID do item do catálogo.
        comprador_ids (List[int]): Lista de IDs dos compradores.
    
    Returns:
        Optional[ItensCatalogo]: Item atualizado com os compradores associados.
    """
    logger.info(f"Associando compradores {comprador_ids} ao item {item_id}")
    
    try:
        # Buscar o item com relacionamentos carregados
        query = (
            select(ItensCatalogo)
            .options(selectinload(ItensCatalogo.compradores))
            .where(ItensCatalogo.id == item_id)
        )
        result = await db.execute(query)
        item = result.scalar_one_or_none()
        
        if not item:
            logger.warning(f"Item com ID {item_id} não encontrado")
            return None
        
        # Buscar usuários compradores
        from app_catalogo.models.user import User
        query_users = select(User).where(User.id.in_(comprador_ids))
        result_users = await db.execute(query_users)
        compradores = result_users.scalars().all()
        
        # Limpar associações existentes e adicionar novas
        item.compradores.clear()
        item.compradores.extend(compradores)
        
        await db.commit()
        await db.refresh(item)
        
        logger.info(f"Compradores associados com sucesso ao item {item_id}")
        return item
        
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Erro ao associar compradores ao item {item_id}: {e}", exc_info=True)
        return None


async def associar_controladores_item(
    db: AsyncSession, 
    item_id: int, 
    controlador_ids: List[int]
) -> Optional[ItensCatalogo]:
    """
    Associa múltiplos controladores a um item do catálogo (relacionamento N:N).
    
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        item_id (int): ID do item do catálogo.
        controlador_ids (List[int]): Lista de IDs dos controladores.
    
    Returns:
        Optional[ItensCatalogo]: Item atualizado com os controladores associados.
    """
    logger.info(f"Associando controladores {controlador_ids} ao item {item_id}")
    
    try:
        # Buscar o item com relacionamentos carregados
        query = (
            select(ItensCatalogo)
            .options(selectinload(ItensCatalogo.controladores))
            .where(ItensCatalogo.id == item_id)
        )
        result = await db.execute(query)
        item = result.scalar_one_or_none()
        
        if not item:
            logger.warning(f"Item com ID {item_id} não encontrado")
            return None
        
        # Buscar usuários controladores
        from app_catalogo.models.user import User
        query_users = select(User).where(User.id.in_(controlador_ids))
        result_users = await db.execute(query_users)
        controladores = result_users.scalars().all()
        
        # Limpar associações existentes e adicionar novas
        item.controladores.clear()
        item.controladores.extend(controladores)
        
        await db.commit()
        await db.refresh(item)
        
        logger.info(f"Controladores associados com sucesso ao item {item_id}")
        return item
        
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Erro ao associar controladores ao item {item_id}: {e}", exc_info=True)
        return None


async def listar_compradores_item(
    db: AsyncSession, 
    item_id: int
) -> List[Dict[str, Any]]:
    """
    Lista todos os compradores associados a um item.
    
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        item_id (int): ID do item do catálogo.
    
    Returns:
        List[Dict[str, Any]]: Lista de compradores associados.
    """
    logger.info(f"Listando compradores do item {item_id}")
    
    try:
        query = (
            select(ItensCatalogo)
            .options(selectinload(ItensCatalogo.compradores))
            .where(ItensCatalogo.id == item_id)
        )
        result = await db.execute(query)
        item = result.scalar_one_or_none()
        
        if not item:
            logger.warning(f"Item com ID {item_id} não encontrado")
            return []
        
        compradores = [
            {
                "id": comprador.id,
                "nome": comprador.nome,
                "email": comprador.email,
                "unidade": comprador.unidade
            }
            for comprador in item.compradores
        ]
        
        logger.info(f"Encontrados {len(compradores)} compradores para o item {item_id}")
        return compradores
        
    except SQLAlchemyError as e:
        logger.error(f"Erro ao listar compradores do item {item_id}: {e}", exc_info=True)
        return []


async def listar_controladores_item(
    db: AsyncSession, 
    item_id: int
) -> List[Dict[str, Any]]:
    """
    Lista todos os controladores associados a um item.
    
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        item_id (int): ID do item do catálogo.
    
    Returns:
        List[Dict[str, Any]]: Lista de controladores associados.
    """
    logger.info(f"Listando controladores do item {item_id}")
    
    try:
        query = (
            select(ItensCatalogo)
            .options(selectinload(ItensCatalogo.controladores))
            .where(ItensCatalogo.id == item_id)
        )
        result = await db.execute(query)
        item = result.scalar_one_or_none()
        
        if not item:
            logger.warning(f"Item com ID {item_id} não encontrado")
            return []
        
        controladores = [
            {
                "id": controlador.id,
                "nome": controlador.nome,
                "email": controlador.email,
                "unidade": controlador.unidade
            }
            for controlador in item.controladores
        ]
        
        logger.info(f"Encontrados {len(controladores)} controladores para o item {item_id}")
        return controladores
        
    except SQLAlchemyError as e:
        logger.error(f"Erro ao listar controladores do item {item_id}: {e}", exc_info=True)
        return []