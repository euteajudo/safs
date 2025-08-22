
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from sqlalchemy.exc import IntegrityError

# Importa os módulos e classes que preparamos
from app_catalogo.models.user import User
from app_catalogo.db_repository.conex_db import get_db
from app_catalogo.db_repository.user_repository import UserRepository
from app_catalogo.schemas.user import UserCreate, UserUpdate, User as UserRead
from app_catalogo.utils import security

# Configura um logger específico para este módulo
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Usuários"])

@router.get(
    "/stats",
    status_code=status.HTTP_200_OK,
    summary="Obtém estatísticas dos usuários"
)
async def get_users_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Retorna estatísticas sobre os usuários do sistema."""
    from sqlalchemy import select, func
    
    # Total de usuários
    total_stmt = select(func.count(User.id))
    total_result = await db.execute(total_stmt)
    total = total_result.scalar() or 0
    
    # Usuários ativos
    active_stmt = select(func.count(User.id)).where(User.is_active == True)
    active_result = await db.execute(active_stmt)
    active = active_result.scalar() or 0
    
    # Novos usuários (últimos 30 dias)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_stmt = select(func.count(User.id)).where(User.created_at >= thirty_days_ago)
    new_result = await db.execute(new_stmt)
    new_users = new_result.scalar() or 0
    
    return {
        "total": total,
        "active": active,
        "inactive": total - active,
        "new_last_30_days": new_users,
        "growth_percentage": round((new_users / total * 100) if total > 0 else 0, 2)
    }

@router.post(
    "", 
    response_model=UserRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuário"
)
async def create_user(
    user_data: UserCreate, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Cria um novo usuário de forma segura."""
    
    logger.info(f"Recebida requisição para criar usuário com email: {user_data.email}")
    user_repo = UserRepository(db)
    try:
        new_user = await user_repo.criar_usuario(user_data.model_dump())
        logger.info(f"Usuário ID {new_user.id} criado com sucesso.")
        return new_user
    except IntegrityError as e:
        logger.warning(f"Falha ao criar usuário. Email ou username já podem existir. Retornando 409.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Usuário com este email ou username já existe.",
        )
    except Exception as e:
        logger.error(f"Erro inesperado ao criar usuário: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}",
        )

@router.get(
    "", 
    response_model=List[UserRead],
    status_code=status.HTTP_200_OK,
    summary="Lista usuários com paginação"
)
async def list_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0, 
    limit: int = 100
):
    """Lista todos os usuários com paginação."""
    logger.info(f"Recebida requisição para listar usuários. Página(skip={skip}, limit={limit})")
    user_repo = UserRepository(db)
    users = await user_repo.listar_usuarios_paginados(skip=skip, limit=limit)
    logger.debug(f"Retornando {len(users)} usuários.")
    return users

@router.get(
    "/me", 
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Obtém dados do usuário autenticado"
)
async def read_users_me(
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Retorna os dados do usuário autenticado."""
    logger.info(f"Usuário ID {current_user.id} ({current_user.email}) acessou seus próprios dados via /me.")
    return current_user

@router.get(
    "/{user_id}", 
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Obtém um usuário por ID"
)
async def get_user_by_id(
    user_id: int, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Obtém um usuário específico por ID."""
    logger.info(f"Recebida requisição para buscar usuário com ID: {user_id}")
    user_repo = UserRepository(db)
    user = await user_repo.pesquisar_usuario_por_id(user_id)
    if user is None:
        logger.warning(f"Usuário com ID {user_id} não encontrado. Retornando 404.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user

@router.patch(
    "/{user_id}", 
    response_model=UserRead,
    status_code=status.HTTP_200_OK, # <-- STATUS CODE EXPLÍCITO
    summary="Atualiza um usuário"
)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Atualiza um usuário existente (requer autenticação)."""
    # <-- NOVO LOG de auditoria
    logger.info(f"Usuário ID {current_user.id} tentando atualizar o usuário ID {user_id}.")
    
    if user_id != current_user.id and not current_user.is_superuser:
        # <-- NOVO LOG de segurança
        logger.warning(f"Acesso negado: Usuário ID {current_user.id} tentou atualizar usuário ID {user_id} sem permissão.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente")
        
    update_data = user_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização.")

    user_repo = UserRepository(db)
    updated_user = await user_repo.atualizar_usuario(user_id, update_data)
    
    if updated_user is None:
        # <-- NOVO LOG
        logger.warning(f"Usuário com ID {user_id} não encontrado para atualização. Retornando 404.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado para atualização"
        )
    
    # <-- NOVO LOG
    logger.info(f"Usuário ID {user_id} atualizado com sucesso por {current_user.id}.")
    return updated_user

@router.delete(
    "/{user_id}", 
    status_code=status.HTTP_204_NO_CONTENT, # <-- STATUS CODE EXPLÍCITO
    summary="Remove um usuário"
)
async def delete_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Remove um usuário (requer autenticação de superuser, chefe de unidade ou chefe de setor)."""
    # <-- NOVO LOG de auditoria
    logger.info(f"Usuário ID {current_user.id} tentando remover o usuário ID {user_id}.")

    # Verificar permissões: superusuário, chefe de unidade ou chefe de setor
    if not (current_user.is_superuser or current_user.is_chefe_unidade or current_user.is_chefe_setor):
        # <-- NOVO LOG de segurança
        logger.warning(f"Acesso negado: Usuário ID {current_user.id} tentou remover usuário ID {user_id} sem permissões adequadas.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Apenas superusuários, chefes de unidade ou chefes de setor podem remover usuários")
        
    user_repo = UserRepository(db)
    success = await user_repo.deletar_usuario(user_id)
    if not success:
        # <-- NOVO LOG
        logger.warning(f"Usuário com ID {user_id} não encontrado para remoção. Retornando 404.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado para remoção"
        )

@router.get(
    "/unidade/{unidade}",
    response_model=List[UserRead],
    status_code=status.HTTP_200_OK,
    summary="Lista usuários por unidade"
)
async def list_users_by_unidade(
    unidade: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Lista usuários por unidade."""
    logger.info(f"Recebida requisição para listar usuários por unidade: {unidade}")
    user_repo = UserRepository(db)
    users = await user_repo.pesquisar_usuarios_por_unidade(unidade)
    logger.debug(f"Retornando {len(users)} usuários.")
    # <-- NOVO LOG
    logger.info(f"Usuário ID {user_id} removido com sucesso por {current_user.id}.")
    return None