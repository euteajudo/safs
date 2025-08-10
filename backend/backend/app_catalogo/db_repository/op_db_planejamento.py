"""Funções de operação com a tabela de planejamento"""

import logging
from typing import Any, List, Optional, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app_catalogo.models.catalogo import ItensCatalogo
from app_catalogo.models.controle_processo import PlanejamentoAquisicao
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import selectinload



logger = logging.getLogger("db_repository")


class ProcessoRepository:
    """Repository class for planning process operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def criar_processo(self, proc_data: dict) -> PlanejamentoAquisicao:
        """Creates a new planning process."""
        return await criar_processo(self.db, proc_data)
    
    async def listar_processos_paginados(self, skip: int = 0, limit: int = 20) -> List[PlanejamentoAquisicao]:
        """Returns a paginated list of planning processes."""
        return await listar_processos_paginados(self.db, skip, limit)
    
    async def pesquisar_processo_por_id(self, proc_id: int) -> Optional[PlanejamentoAquisicao]:
        """Searches for a process by ID."""
        return await pesquisar_processo_por_id(self.db, proc_id)
    
    async def atualizar_processo(self, proc_id: int, updates: Dict[str, Any]) -> Optional[PlanejamentoAquisicao]:
        """Updates a process by ID."""
        return await atualizar_processo(self.db, proc_id, updates)
    
    async def deletar_processo(self, proc_id: int) -> bool:
        """Deletes a process by ID."""
        return await deletar_processo(self.db, proc_id)
    
    async def pesquisar_processo_por_numero(self, numero_processo: str) -> Optional[PlanejamentoAquisicao]:
        """Searches for a process by planning process number."""
        return await pesquisar_processo_por_numero(self.db, numero_processo)
    
    async def pesquisar_processos_por_codigo_master(self, proc_codigo_master: str) -> List[PlanejamentoAquisicao]:
        """Searches for all processes by master code."""
        return await pesquisar_processos_por_codigo_master(self.db, proc_codigo_master)
    
    async def pesquisar_por_numero_compra(self, numero_compra: str) -> Optional[PlanejamentoAquisicao]:
        """Searches for a process by purchase number."""
        return await pesquisar_por_numero_compra(self.db, numero_compra)
    
    async def atualizar_processo_por_numero(self, numero_processo: str, updates: Dict[str, Any]) -> Optional[PlanejamentoAquisicao]:
        """Updates a process by planning process number."""
        return await atualizar_processo_por_numero(self.db, numero_processo, updates)
    
    async def listar_itens_por_numero_processo(self, numero_processo: str, skip: int = 0, limit: int = 100) -> list[ItensCatalogo]:
        """Returns all catalog items associated with the given process number."""
        return await listar_itens_por_numero_processo(self.db, numero_processo, skip, limit)
    
    async def pesquisar_processos_por_unidade(self, unidade: str) -> List[PlanejamentoAquisicao]:
        """Searches for all processes by unit."""
        return await pesquisar_processos_por_unidade(self.db, unidade)


async def criar_processo(db: AsyncSession, proc_data: dict) -> PlanejamentoAquisicao:
    """
    Insere um novo processo de planejamento.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        proc_data (dict): Dados do processo.
    Returns:
        PlanejamentoAquisicao: Processo criado.
    Raises:
        IntegrityError: Se o processo já existir.
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Inserindo processo de planejamento: {proc_data}")
    # Cria a instância fora do try para validar os dados do dict primeiro (opcional)
    try:
        proc = PlanejamentoAquisicao(**proc_data)
    except TypeError as e:
        logger.error(f"Erro de tipo ao criar instância do modelo: {e}", exc_info=True)
        # Re-levantamos o erro para a camada de serviço/API tratar
        raise

    try:
        db.add(proc)
        await db.commit()
        await db.refresh(proc)
        
        logger.info(f"Processo criado com sucesso. ID: {proc.id}")
        return proc

    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao criar processo. Possível duplicidade. {e}")
        # É crucial fazer o rollback para limpar a sessão
        await db.rollback()
        # Re-levanta a exceção para que a camada da API possa retornar um erro 409 Conflict
        raise e

    except SQLAlchemyError as e:
        logger.error(f"Erro inesperado de banco de dados ao criar processo: {e}", exc_info=True)
        # Rollback é obrigatório aqui também
        await db.rollback()
        # Re-levanta a exceção para que a camada da API possa retornar um erro 500 Internal Server Error
        raise e

async def listar_processos_paginados(db: AsyncSession, skip: int = 0, limit: int = 20) -> List[PlanejamentoAquisicao]:
    """
    Retorna uma lista paginada de processos de planejamento.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        skip (int): Número de registros a serem ignorados.
        limit (int): Número máximo de registros a serem retornados.
    Returns:
        List[PlanejamentoAquisicao]: Lista de processos.
    """
    logger.info("Buscando todos os processos de planejamento...Página(skip={skip}, limit={limit})")
    try:
        # A query agora inclui offset (pular) e limit (limitar)
        query = select(PlanejamentoAquisicao).offset(skip).limit(limit)
        
        result = await db.execute(query)
        processos = result.scalars().all()
        
        logger.debug(f"Total de processos encontrados nesta página: {len(processos)}")
        return processos
        
    except SQLAlchemyError as e:
        logger.error(f"Erro de banco de dados ao listar processos: {e}", exc_info=True)
        # Em caso de erro, retorna uma lista vazia para não quebrar o consumidor da função.
        return []




async def pesquisar_processo_por_id(db: AsyncSession, proc_id: int) -> Optional[PlanejamentoAquisicao]:
    """
    Busca um processo pelo ID de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        proc_id (int): ID do processo.
    Returns:
        Optional[PlanejamentoAquisicao]: O processo encontrado ou None se não existir
                                         ou em caso de erro no banco de dados.
    """
    logger.info(f"Buscando processo de planejamento pelo ID: {proc_id}")
    try:
        # A melhor maneira de buscar por chave primária
        proc = await db.get(PlanejamentoAquisicao, proc_id)
        
        if proc:
            logger.debug(f"Processo encontrado: {proc}")
        else:
            logger.warning(f"Processo com ID {proc_id} não encontrado.")
            
        return proc

    except SQLAlchemyError as e:
        logger.error(f"Erro de banco de dados ao buscar processo por ID {proc_id}: {e}", exc_info=True)
        # Retorna None para manter a consistência do tipo de retorno e sinalizar falha
        return None



async def atualizar_processo(db: AsyncSession, proc_id: int, updates: Dict[str, Any]) -> Optional[PlanejamentoAquisicao]:
    """
    Atualiza um processo pelo ID de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        proc_id (int): ID do processo.
        updates (Dict[str, Any]): Dados a serem atualizados.
    Returns:
        Optional[PlanejamentoAquisicao]: O processo atualizado ou None se não existir.
    """
    logger.info(f"Tentando atualizar processo {proc_id} com dados: {updates}")
    
    # A busca inicial também precisa de proteção
    try:
        proc = await db.get(PlanejamentoAquisicao, proc_id)
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar processo {proc_id} para atualização: {e}", exc_info=True)
        return None

    if not proc:
        logger.warning(f"Processo com ID {proc_id} não encontrado para atualização.")
        return None

    # O bloco de atualização e commit é a parte mais crítica
    try:
        for key, value in updates.items():
            # Uma verificação extra de segurança (opcional, mas bom)
            if hasattr(proc, key):
                setattr(proc, key, value)
        
        await db.commit()
        await db.refresh(proc)
        logger.info(f"Processo {proc_id} atualizado com sucesso.")
        return proc

    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao atualizar processo {proc_id}. Possível duplicidade. {e}")
        await db.rollback()
        # Retorna None para indicar que a atualização falhou
        return None
        
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao atualizar processo {proc_id}: {e}", exc_info=True)
        await db.rollback()
        return None

async def deletar_processo(db: AsyncSession, proc_id: int) -> bool:
    """Remove um processo de planejamento pelo ID de forma segura."""
    logger.info(f"Tentando remover processo com ID: {proc_id}")
    
    # A busca inicial também é uma operação de I/O
    try:
        proc = await db.get(PlanejamentoAquisicao, proc_id)
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar processo {proc_id} para remoção: {e}", exc_info=True)
        return False

    if not proc:
        logger.warning(f"Processo com ID {proc_id} não encontrado para remoção.")
        return False

    try:
        await db.delete(proc)
        await db.commit()
        logger.info(f"Processo {proc_id} removido com sucesso.")
        return True

    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao remover processo {proc_id}. Pode ser uma violação de FK. {e}", exc_info=True)
        await db.rollback()
        # A remoção não teve sucesso, então retornamos False.
        return False
    
async def pesquisar_processo_por_numero(db: AsyncSession, numero_processo: str) -> Optional[PlanejamentoAquisicao]:
    """Busca um processo pelo número de forma segura."""
    logger.info(f"Buscando processo pelo número: {numero_processo}")
    try:
        query = select(PlanejamentoAquisicao).where(PlanejamentoAquisicao.numero_processo_planejamento == numero_processo)
        result = await db.execute(query)
        
        # .first() é mais seguro pois retorna o primeiro encontrado ou None, 
        # sem levantar erro se houver múltiplos resultados.
        proc = result.scalars().first()

        if proc:
            logger.debug(f"Processo encontrado: {proc}")
        else:
            logger.warning(f"Processo com número {numero_processo} não encontrado.")
        
        return proc

    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar processo por número {numero_processo}: {e}", exc_info=True)
        # Retorna None para sinalizar falha ou ausência
        return None




async def pesquisar_processos_por_codigo_master( # Nome no plural para clareza
    db: AsyncSession, 
    proc_codigo_master: str
) -> List[PlanejamentoAquisicao]: # Tipo de retorno é uma Lista
    """
    Realiza uma busca por todos os processos de planejamento que contêm um item
    com o código master especificado.

    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        proc_codigo_master (str): Código master do item a ser buscado.

    Returns:
        List[PlanejamentoAquisicao]: Uma lista com todos os processos encontrados.
                                     Retorna uma lista vazia se nenhum for encontrado
                                     ou em caso de erro no banco de dados.
    """
    logger.info(f"Buscando todos os processos de planejamento pelo código master: {proc_codigo_master}")
    try:
        query = select(PlanejamentoAquisicao).where(PlanejamentoAquisicao.codigo_master == proc_codigo_master)
        
        resultado = await db.execute(query)
        
        # O método .all() coleta todos os resultados em uma lista.
        # Se não houver resultados, ele retorna uma lista vazia [].
        processos = resultado.scalars().all()

        if processos:
            # O log agora informa a quantidade de processos encontrados.
            logger.debug(f"{len(processos)} processo(s) encontrado(s) para o código master {proc_codigo_master}.")
        else:
            # O warning continua relevante para o caso de não encontrar nenhum.
            logger.warning(f"Nenhum processo encontrado com o código master {proc_codigo_master}.")
        
        return processos

    except SQLAlchemyError as e:
        logger.error(f"Erro no banco de dados ao buscar por código master {proc_codigo_master}: {e}", exc_info=True)
        # Retorna uma lista vazia para manter a consistência do tipo de retorno da função.
        return []




async def pesquisar_por_numero_compra(
    db: AsyncSession, 
    numero_compra: str
) -> Optional[PlanejamentoAquisicao]:
    """
    Busca um processo pelo número de compra centralizada de forma segura.

    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        numero_compra (str): O número do processo de compra centralizada.

    Returns:
        Optional[PlanejamentoAquisicao]: O processo encontrado ou None se não existir
                                         ou em caso de erro no banco de dados.
    """
    logger.info(f"Buscando processo pelo número de compra centralizada: {numero_compra}")
    try:
        query = select(PlanejamentoAquisicao).where(
            PlanejamentoAquisicao.numero_processo_compra_centralizada == numero_compra
        )
        result = await db.execute(query)
        
        # .first() é mais seguro, evitando o erro 'MultipleResultsFound'.
        proc = result.scalars().first()

        if proc:
            logger.debug(f"Processo encontrado para o número de compra '{numero_compra}': {proc}")
        else:
            logger.warning(f"Nenhum processo encontrado com o número de compra '{numero_compra}'.")
            
        return proc

    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar por número de compra '{numero_compra}': {e}", exc_info=True)
        # Retorna None para manter o contrato da função e sinalizar falha.
        return None




async def atualizar_processo_por_numero(
    db: AsyncSession, 
    numero_processo: str, 
    updates: Dict[str, Any]
) -> Optional[PlanejamentoAquisicao]:
    """
    Atualiza um processo buscando-o pelo número do processo de planejamento.

    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        numero_processo (str): O número do processo de planejamento a ser atualizado.
        updates (Dict[str, Any]): Um dicionário com os campos a serem atualizados.

    Returns:
        Optional[PlanejamentoAquisicao]: O objeto do processo atualizado, ou None se
                                         o processo não for encontrado ou se ocorrer um erro.
    """
    logger.info(f"Tentando atualizar processo pelo número '{numero_processo}' com dados: {updates}")

    # Envolve toda a operação em um bloco try/except para capturar erros de conexão
    try:
        # --- Passo 1: Buscar o processo pelo número ---
        query = select(PlanejamentoAquisicao).where(PlanejamentoAquisicao.numero_processo_planejamento == numero_processo)
        result = await db.execute(query)
        proc = result.scalars().first()  # Usar .first() para segurança

        if not proc:
            logger.warning(f"Processo com número '{numero_processo}' não encontrado para atualização.")
            return None

        # --- Passo 2: Aplicar as atualizações e fazer o commit ---
        for key, value in updates.items():
            if hasattr(proc, key):
                setattr(proc, key, value)
        
        await db.commit()
        await db.refresh(proc)
        
        logger.info(f"Processo com número '{numero_processo}' (ID: {proc.id}) atualizado com sucesso.")
        return proc

    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao atualizar processo '{numero_processo}'. Possível duplicidade em campo único. {e}")
        await db.rollback()
        return None  # Retorna None para indicar que a atualização falhou
        
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB inesperado ao atualizar processo '{numero_processo}': {e}", exc_info=True)
        await db.rollback()
        return None  # Retorna None em caso de qualquer outro erro de DB
    

async def pesquisar_processos_por_unidade(db: AsyncSession, unidade: str) -> List[PlanejamentoAquisicao]:
    """Busca processos por unidade de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        unidade (str): Unidade do processo.
    Returns:
        List[PlanejamentoAquisicao]: Lista de processos encontrados.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Buscando processos por unidade: {unidade}")
    try:
        query = select(PlanejamentoAquisicao).where(PlanejamentoAquisicao.unidade == unidade)
        result = await db.execute(query)
        return result.scalars().all()

    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar processos por unidade {unidade}: {e}", exc_info=True)
        return []


async def listar_itens_por_numero_processo(
    session: AsyncSession, 
    numero_processo: str,
    skip: int = 0,
    limit: int = 100
) -> list[ItensCatalogo]:
    """
    Retorna todos os itens do catálogo associados ao número do processo de planejamento informado,
    de forma segura e paginada.
    Args:
        session (AsyncSession): Sessão assíncrona SQLAlchemy.
        numero_processo (str): Número do processo de planejamento.
        skip (int): Número de registros a serem ignorados.
        limit (int): Número máximo de registros a serem retornados.
    Returns:
        list[ItensCatalogo]: Lista de itens do catálogo associados ao processo.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Buscando itens para o processo '{numero_processo}'... Página(skip={skip}, limit={limit})")
    try:
        # --- LÓGICA CORRIGIDA COM JOIN ---
        query = (
            select(ItensCatalogo)
            # Faz o JOIN com a tabela PlanejamentoAquisicao através do relacionamento
            .join(ItensCatalogo.processo)
            # Filtra pela coluna correta na tabela correta
            .where(PlanejamentoAquisicao.numero_processo_planejamento == numero_processo)
            .offset(skip)
            .limit(limit)
        )
        
        result = await session.execute(query)
        return result.scalars().all()

    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar itens para o processo '{numero_processo}': {e}", exc_info=True)
        return []