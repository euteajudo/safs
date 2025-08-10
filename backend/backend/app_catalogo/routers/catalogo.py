"""Rotas para o catálogo de itens"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from sqlalchemy.exc import IntegrityError

from app_catalogo.models.catalogo import ItensCatalogo  
from app_catalogo.models.user import User
from app_catalogo.schemas import catalogo as catalogo_schemas
from app_catalogo.db_repository.conex_db import get_db
from app_catalogo.db_repository.op_db_catalogo import ItemCatalogoRepository
from app_catalogo.utils import security

logger = logging.getLogger(__name__)

router = APIRouter(
    
    tags=["Catálogo de Itens"],
    dependencies=[Depends(security.get_current_active_user)]
)

@router.get(
    "/stats",
    status_code=status.HTTP_200_OK,
    summary="Obtém estatísticas do catálogo"
)
async def get_catalog_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Retorna estatísticas sobre os itens do catálogo."""
    from sqlalchemy import select, func
    
    # Total de itens
    total_stmt = select(func.count(ItensCatalogo.id))
    total_result = await db.execute(total_stmt)
    total = total_result.scalar() or 0
    
    # Itens por classificação
    class_stmt = select(
        ItensCatalogo.classificacao_xyz,
        func.count(ItensCatalogo.id)
    ).group_by(ItensCatalogo.classificacao_xyz)
    class_result = await db.execute(class_stmt)
    items_by_classification = {row[0]: row[1] for row in class_result if row[0]}
    
    # Novos itens (últimos 30 dias)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_stmt = select(func.count(ItensCatalogo.id)).where(ItensCatalogo.created_at >= thirty_days_ago)
    new_result = await db.execute(new_stmt)
    new_items = new_result.scalar() or 0
    
    return {
        "total": total,
        "by_classification": items_by_classification,
        "new_last_30_days": new_items,
        "growth_percentage": round((new_items / total * 100) if total > 0 else 0, 2),
        "types_count": len(items_by_classification)
    }

# --- MÉTODO POST ---

@router.post(
    "/", 
    response_model=catalogo_schemas.ItemCatalogoRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo item no catálogo"
)
async def create_item(
    item_data: catalogo_schemas.ItemCatalogoCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Cria um novo item no catálogo."""
    logger.info(f"Usuário {current_user.email} tentando criar item: {item_data.codigo_master}")
    repo = ItemCatalogoRepository(db)
    try:
        novo_item = await repo.criar_item(item_data.model_dump())
        logger.info(f"Item ID {novo_item.id} criado com sucesso.")
        return novo_item
    except IntegrityError:
        logger.warning(f"Falha ao criar item. Código master '{item_data.codigo_master}' já existe ou FK inválida.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Item com código master '{item_data.codigo_master}' já existe ou ID de relacionamento inválido.",
        )

# --- MÉTODOS GET ---

@router.get(
    "/", 
    response_model=List[catalogo_schemas.ItemCatalogoRead],
    summary="Lista todos os itens do catálogo"
)
async def list_items(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    """Retorna uma lista paginada de todos os itens do catálogo."""
    repo = ItemCatalogoRepository(db)
    # A função do repo já otimiza o carregamento dos relacionamentos.
    # O Pydantic e o response_model fazem o resto da mágica.
    itens = await repo.listar_itens_paginados(skip=skip, limit=limit)
    return itens

@router.get(
    "/{item_id}", 
    response_model=catalogo_schemas.ItemCatalogoRead,
    summary="Busca um item por seu ID"
)
async def get_item_by_id(
    item_id: int, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Retorna os detalhes de um item específico pelo seu ID."""
    repo = ItemCatalogoRepository(db)
    item = await repo.pesquisar_item_por_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado")
    return item

@router.get(
    "/codigo_master/{codigo_master}", 
    response_model=catalogo_schemas.ItemCatalogoRead,
    summary="Busca um item pelo seu Código Master"
)
async def get_item_by_codigo_master(
    codigo_master: str, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Retorna os detalhes de um item pelo seu Código Master único."""
    repo = ItemCatalogoRepository(db)
    item = await repo.pesquisar_item_por_codigo_master(codigo_master)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado")
    return item

# --- MÉTODO PATCH ---

@router.patch(
    "/{item_id}", 
    response_model=catalogo_schemas.ItemCatalogoRead,
    summary="Atualiza um item do catálogo"
)
async def update_item(
    item_id: int,
    item_update: catalogo_schemas.ItemCatalogoUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Atualiza parcialmente os dados de um item do catálogo."""
    logger.info(f"Usuário {current_user.email} tentando atualizar o item ID {item_id}")
    repo = ItemCatalogoRepository(db)
    update_data = item_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização.")
    
    updated_item = await repo.atualizar_item(item_id, update_data)
    
    if updated_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado ou falha na atualização"
        )
    return updated_item

# --- MÉTODO DELETE ---

@router.delete(
    "/{item_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um item do catálogo"
)
async def delete_item(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Remove um item do catálogo (requer permissão de superusuário)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Apenas superusuários podem remover itens do catálogo")
    
    logger.info(f"Superusuário {current_user.email} tentando remover o item ID {item_id}")
    repo = ItemCatalogoRepository(db)
    success = await repo.deletar_item(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado para remoção"
        )
    return None
