"""Função de operações com usuários no banco de dados"""

import logging
from typing import Any, List, Optional, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app_catalogo.models.user import User
from sqlalchemy import func
from app_catalogo.utils.security import get_password_hash 
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime, timezone

logger = logging.getLogger("db_repository")






async def criar_usuario(db: AsyncSession, user_data: dict) -> User:
    """Insere um novo usuário de forma segura, com hashing de senha.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        user_data (dict): Dados do usuário.
    Returns:
        User: Usuário criado.
    Raises:
        IntegrityError: Se o usuário já existir.
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Tentando inserir usuário: {user_data.get('email')}")
    
    # Copia os dados para não modificar o dicionário original
    user_create_data = user_data.copy()

    # --- MELHORIA DE SEGURANÇA ---
    # Hashear a senha antes de criar o objeto
    hashed_password = get_password_hash(user_create_data.pop("senha"))
    user_create_data["senha"] = hashed_password
    
    user = User(**user_create_data)

    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Usuário criado com sucesso. ID: {user.id}")
        return user
    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao criar usuário. Email '{user_data.get('email')}' já pode existir. {e}")
        await db.rollback()
        raise e  # Re-levanta para a API tratar como 409 Conflict
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao criar usuário: {e}", exc_info=True)
        await db.rollback()
        raise e

async def listar_usuarios_paginados(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    """Retorna uma lista paginada de usuários de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        skip (int): Número de registros a serem ignorados.
        limit (int): Número máximo de registros a serem retornados.
    Returns:
        List[User]: Lista de usuários.
    """
    logger.info(f"Buscando usuários... Página(skip={skip}, limit={limit})")
    try:
        query = select(User).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao listar usuários: {e}", exc_info=True)
        return []

async def pesquisar_usuario_por_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Busca um usuário pelo ID de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        user_id (int): ID do usuário.
    Returns:
        Optional[User]: Usuário encontrado ou None.
    """
    logger.info(f"Buscando usuário pelo ID: {user_id}")
    try:
        return await db.get(User, user_id)
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar usuário por ID {user_id}: {e}", exc_info=True)
        return None


async def atualizar_usuario(db: AsyncSession, user_id: int, updates: Dict[str, Any]) -> Optional[User]:
    """Atualiza um usuário pelo ID de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        user_id (int): ID do usuário.
        updates (Dict[str, Any]): Dados a serem atualizados.
    Returns:
        Optional[User]: Usuário atualizado ou None.
    Raises:
        IntegrityError: Se o usuário já existir.
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    try:
        user = await db.get(User, user_id)
        if not user:
            logger.warning(f"Usuário com ID {user_id} não encontrado para atualização.")
            return None

        update_data = updates.copy()

        # --- MELHORIA DE SEGURANÇA ---
        if "senha" in update_data and update_data["senha"]:
            hashed_password = get_password_hash(update_data.pop("senha"))
            update_data["senha"] = hashed_password
        
        for key, value in update_data.items():
            setattr(user, key, value)
        
        # --- MELHORIA DE LÓGICA ---
        user.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        
        await db.commit()
        await db.refresh(user)
        logger.info(f"Usuário {user_id} atualizado com sucesso.")
        return user
    except IntegrityError as e:
        logger.warning(f"Erro de integridade ao atualizar usuário {user_id}. Email já pode existir. {e}")
        await db.rollback()
        return None
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao atualizar usuário {user_id}: {e}", exc_info=True)
        await db.rollback()
        return None

async def deletar_usuario(db: AsyncSession, user_id: int) -> bool:
    """Remove um usuário pelo ID de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        user_id (int): ID do usuário.
    Returns:
        bool: True se removido, False se não encontrado.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    try:
        user = await db.get(User, user_id)
        if not user:
            logger.warning(f"Usuário com ID {user_id} não encontrado para remoção.")
            return False
        
        await db.delete(user)
        await db.commit()
        logger.info(f"Usuário {user_id} removido com sucesso.")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao remover usuário {user_id}: {e}", exc_info=True)
        await db.rollback()
        return False
    


async def pesquisar_usuario_por_nome(db: AsyncSession, user_nome: str) -> Optional[User]:
    """Busca um usuário pelo nome (parcial, case-insensitive) de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        user_nome (str): Nome (ou parte do nome) do usuário.
    Returns:
        Optional[User]: Primeiro usuário encontrado ou None.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Buscando usuário por nome: {user_nome}")
    try:
        stmt = select(User).where(func.lower(User.nome).like(f"%{user_nome.lower()}%"))
        result = await db.execute(stmt)
        return result.scalars().first()
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar usuário por nome {user_nome}: {e}", exc_info=True)
        return None


async def pesquisar_usuario_por_email(db: AsyncSession, email: str) -> Optional[User]:
    """Busca um usuário pelo email (campo único) de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        email (str): Email do usuário.
    Returns:
        Optional[User]: Usuário encontrado ou None.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Buscando usuário por email: {email}")
    try:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        return result.scalars().first()
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar usuário por email {email}: {e}", exc_info=True)
        return None


async def pesquisar_usuario_por_username(db: AsyncSession, username: str) -> Optional[User]:
    """Busca um usuário pelo username (campo único) de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        username (str): Username do usuário.
    Returns:
        Optional[User]: Usuário encontrado ou None.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Buscando usuário por username: {username}")
    try:
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        return result.scalars().first()
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar usuário por username {username}: {e}", exc_info=True)
        return None

async def pesquisar_usuarios_por_unidade(db: AsyncSession, unidade: str) -> List[User]:
    """Busca usuários por unidade de forma segura.
    Args:
        db (AsyncSession): Sessão assíncrona SQLAlchemy.
        unidade (str): Unidade do usuário.
    Returns:
        List[User]: Lista de usuários encontrados.
    Raises:
        SQLAlchemyError: Se houver outro erro no banco de dados.
    """
    logger.info(f"Buscando usuários por unidade: {unidade}")
    try:
        stmt = select(User).where(User.unidade == unidade)
        result = await db.execute(stmt)
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Erro de DB ao buscar usuários por unidade {unidade}: {e}", exc_info=True)
        return []