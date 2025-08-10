"""Classe repositório para operações com usuários no banco de dados"""

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


class UserRepository:
    """Repositório para operações com usuários"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def criar_usuario(self, user_data: dict) -> User:
        """Insere um novo usuário de forma segura, com hashing de senha.
        Args:
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
        
        # --- VALIDAÇÃO DE UNICIDADE ---
        # Verifica se email já existe
        existing_user = await self.pesquisar_por_email(user_create_data.get('email'))
        if existing_user:
            logger.warning(f"Email '{user_create_data.get('email')}' já existe.")
            raise IntegrityError("Email já existe", None, None)
        
        # Verifica se username já existe
        existing_username = await self.pesquisar_por_username(user_create_data.get('username'))
        if existing_username:
            logger.warning(f"Username '{user_create_data.get('username')}' já existe.")
            raise IntegrityError("Username já existe", None, None)

        # --- MELHORIA DE SEGURANÇA ---
        # Hashear a senha antes de criar o objeto
        hashed_password = get_password_hash(user_create_data.pop("senha"))
        user_create_data["senha"] = hashed_password
        
        # Remove campos que são gerados automaticamente pelo modelo
        user_create_data.pop("created_at", None)
        user_create_data.pop("updated_at", None)
        
        user = User(**user_create_data)

        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            logger.info(f"Usuário criado com sucesso. ID: {user.id}")
            return user
        except IntegrityError as e:
            logger.warning(f"Erro de integridade ao criar usuário. Email '{user_data.get('email')}' já pode existir. {e}")
            await self.db.rollback()
            raise e  # Re-levanta para a API tratar como 409 Conflict
        except SQLAlchemyError as e:
            logger.error(f"Erro de DB ao criar usuário: {e}", exc_info=True)
            await self.db.rollback()
            raise e

    async def listar_usuarios_paginados(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Retorna uma lista paginada de usuários de forma segura.
        Args:
            skip (int): Número de registros a serem ignorados.
            limit (int): Número máximo de registros a serem retornados.
        Returns:
            List[User]: Lista de usuários.
        """
        logger.info(f"Buscando usuários... Página(skip={skip}, limit={limit})")
        try:
            query = select(User).offset(skip).limit(limit)
            result = await self.db.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Erro de DB ao listar usuários: {e}", exc_info=True)
            return []

    async def pesquisar_usuario_por_id(self, user_id: int) -> Optional[User]:
        """Busca um usuário pelo ID de forma segura.
        Args:
            user_id (int): ID do usuário.
        Returns:
            Optional[User]: Usuário encontrado ou None.
        """
        logger.info(f"Buscando usuário pelo ID: {user_id}")
        try:
            return await self.db.get(User, user_id)
        except SQLAlchemyError as e:
            logger.error(f"Erro de DB ao buscar usuário por ID {user_id}: {e}", exc_info=True)
            return None

    async def atualizar_usuario(self, user_id: int, updates: Dict[str, Any]) -> Optional[User]:
        """Atualiza um usuário pelo ID de forma segura.
        Args:
            user_id (int): ID do usuário.
            updates (Dict[str, Any]): Dados a serem atualizados.
        Returns:
            Optional[User]: Usuário atualizado ou None.
        Raises:
            IntegrityError: Se o usuário já existir.
            SQLAlchemyError: Se houver outro erro no banco de dados.
        """
        try:
            user = await self.db.get(User, user_id)
            if not user:
                logger.warning(f"Usuário com ID {user_id} não encontrado para atualização.")
                return None

            update_data = updates.copy()
            
            # --- VALIDAÇÃO DE UNICIDADE ---
            # Verifica se email já existe (exceto para o próprio usuário)
            if "email" in update_data:
                existing_user = await self.pesquisar_por_email(update_data["email"])
                if existing_user and existing_user.id != user_id:
                    logger.warning(f"Email '{update_data['email']}' já está em uso por outro usuário.")
                    raise IntegrityError("Email já existe", None, None)
            
            # Verifica se username já existe (exceto para o próprio usuário)
            if "username" in update_data:
                existing_username = await self.pesquisar_por_username(update_data["username"])
                if existing_username and existing_username.id != user_id:
                    logger.warning(f"Username '{update_data['username']}' já está em uso por outro usuário.")
                    raise IntegrityError("Username já existe", None, None)

            # --- MELHORIA DE SEGURANÇA ---
            if "senha" in update_data and update_data["senha"]:
                hashed_password = get_password_hash(update_data.pop("senha"))
                update_data["senha"] = hashed_password
            
            for key, value in update_data.items():
                setattr(user, key, value)
            
            # --- MELHORIA DE LÓGICA ---
            user.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            
            await self.db.commit()
            await self.db.refresh(user)
            logger.info(f"Usuário {user_id} atualizado com sucesso.")
            return user
        except IntegrityError as e:
            logger.warning(f"Erro de integridade ao atualizar usuário {user_id}. Email já pode existir. {e}")
            await self.db.rollback()
            return None
        except SQLAlchemyError as e:
            logger.error(f"Erro de DB ao atualizar usuário {user_id}: {e}", exc_info=True)
            await self.db.rollback()
            return None

    async def deletar_usuario(self, user_id: int) -> bool:
        """Remove um usuário pelo ID de forma segura.
        Args:
            user_id (int): ID do usuário.
        Returns:
            bool: True se removido, False se não encontrado.
        Raises:
            SQLAlchemyError: Se houver outro erro no banco de dados.
        """
        try:
            user = await self.db.get(User, user_id)
            if not user:
                logger.warning(f"Usuário com ID {user_id} não encontrado para remoção.")
                return False
            
            await self.db.delete(user)
            await self.db.commit()
            logger.info(f"Usuário {user_id} removido com sucesso.")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Erro de DB ao remover usuário {user_id}: {e}", exc_info=True)
            await self.db.rollback()
            return False

    async def pesquisar_por_email(self, email: str) -> Optional[User]:
        """Busca um usuário pelo email (campo único) de forma segura.
        Args:
            email (str): Email do usuário.
        Returns:
            Optional[User]: Usuário encontrado ou None.
        Raises:
            SQLAlchemyError: Se houver outro erro no banco de dados.
        """
        logger.info(f"Buscando usuário por email: {email}")
        try:
            stmt = select(User).where(User.email == email)
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Erro de DB ao buscar usuário por email {email}: {e}", exc_info=True)
            return None

    async def pesquisar_por_username(self, username: str) -> Optional[User]:
        """Busca um usuário pelo username (campo único) de forma segura.
        Args:
            username (str): Username do usuário.
        Returns:
            Optional[User]: Usuário encontrado ou None.
        Raises:
            SQLAlchemyError: Se houver outro erro no banco de dados.
        """
        logger.info(f"Buscando usuário por username: {username}")
        try:
            stmt = select(User).where(User.username == username)
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Erro de DB ao buscar usuário por username {username}: {e}", exc_info=True)
            return None 