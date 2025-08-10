
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from sqlalchemy.exc import IntegrityError

from app_catalogo.models.controle_processo import PlanejamentoAquisicao
from app_catalogo.models.user import User
from app_catalogo.schemas import controle_processos as processo_schemas
from app_catalogo.db_repository.op_db_planejamento import ProcessoRepository 
from app_catalogo.db_repository.conex_db import get_db
from app_catalogo.utils import security

logger = logging.getLogger(__name__)

router = APIRouter(
     
    tags=["Processos de Aquisição"],
    dependencies=[Depends(security.get_current_active_user)]
)

@router.get(
    "/stats",
    status_code=status.HTTP_200_OK,
    summary="Obtém estatísticas dos processos"
)
async def get_processos_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Retorna estatísticas sobre os processos de aquisição."""
    from sqlalchemy import select, func
    
    # Total de processos
    total_stmt = select(func.count(PlanejamentoAquisicao.id))
    total_result = await db.execute(total_stmt)
    total = total_result.scalar() or 0
    
    # Processos por status
    status_stmt = select(
        PlanejamentoAquisicao.status_processo_planejamento,
        func.count(PlanejamentoAquisicao.id)
    ).group_by(PlanejamentoAquisicao.status_processo_planejamento)
    status_result = await db.execute(status_stmt)
    by_status = {row[0]: row[1] for row in status_result if row[0]}
    
    # Novos processos (últimos 30 dias)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_stmt = select(func.count(PlanejamentoAquisicao.id)).where(
        PlanejamentoAquisicao.created_at >= thirty_days_ago
    )
    new_result = await db.execute(new_stmt)
    new_processos = new_result.scalar() or 0
    
    return {
        "total": total,
        "by_status": by_status,
        "new_last_30_days": new_processos,
        "in_progress": by_status.get("Em Andamento", 0),
        "completed": by_status.get("Concluído", 0),
        "growth_percentage": round((new_processos / total * 100) if total > 0 else 0, 2)
    }


@router.post(
    "/", 
    response_model=processo_schemas.ProcessoRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo processo de planejamento"
)
async def create_processo(
    processo_data: processo_schemas.ProcessoCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Cria um novo processo de planejamento no sistema."""
    logger.info(f"Usuário {current_user.email} tentando criar processo: {processo_data.numero_processo_planejamento}")
    repo = ProcessoRepository(db)
    try:
        novo_processo = await repo.criar_processo(processo_data.model_dump())
        logger.info(f"Processo ID {novo_processo.id} criado com sucesso.")
        return novo_processo
    except IntegrityError:
        logger.warning(f"Falha ao criar processo. Número '{processo_data.numero_processo_planejamento}' já existe.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Processo com número '{processo_data.numero_processo_planejamento}' já existe.",
        )

@router.get(
    "/", 
    response_model=List[processo_schemas.ProcessoRead],
    summary="Lista todos os processos de forma paginada"
)
async def list_processos(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    """Retorna uma lista paginada de todos os processos de planejamento."""
    repo = ProcessoRepository(db)
    processos = await repo.listar_processos_paginados(skip=skip, limit=limit)
    return processos

@router.get(
    "/{processo_id}", 
    response_model=processo_schemas.ProcessoRead,
    summary="Busca um processo por seu ID"
)
async def get_processo_by_id(
    processo_id: int, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Retorna os detalhes de um processo específico pelo seu ID."""
    logger.info(f"Buscando processo por ID: {processo_id}")
    repo = ProcessoRepository(db)
    processo = await repo.pesquisar_processo_por_id(processo_id)
    if processo is None:
        logger.warning(f"Processo com ID {processo_id} não encontrado.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Processo não encontrado")
    return processo

@router.get(
    "/numero/{numero_processo}", 
    response_model=processo_schemas.ProcessoRead,
    summary="Busca um processo por seu número"
)
async def get_processo_by_numero(
    numero_processo: str, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Retorna os detalhes de um processo pelo seu número de planejamento."""
    repo = ProcessoRepository(db)
    processo = await repo.pesquisar_processo_por_numero(numero_processo)
    if processo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Processo não encontrado")
    return processo


@router.patch(
    "/{processo_id}", 
    response_model=processo_schemas.ProcessoRead,
    summary="Atualiza um processo existente"
)
async def update_processo(
    processo_id: int,
    processo_update: processo_schemas.ProcessoUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Atualiza parcialmente os dados de um processo de planejamento."""
    logger.info(f"Usuário {current_user.email} tentando atualizar o processo ID {processo_id}")
    repo = ProcessoRepository(db)
    update_data = processo_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado fornecido para atualização.")
    
    updated_processo = await repo.atualizar_processo(processo_id, update_data)
    
    if updated_processo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Processo não encontrado ou falha na atualização"
        )
    return updated_processo

@router.delete(
    "/{processo_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um processo de planejamento"
)
async def delete_processo(
    processo_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Remove um processo (requer permissão de superusuário)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Apenas superusuários podem remover processos")
    
    logger.info(f"Superusuário {current_user.email} tentando remover o processo ID {processo_id}")
    repo = ProcessoRepository(db)
    success = await repo.deletar_processo(processo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Processo não encontrado para remoção"
        )
    return None # Retorna uma resposta vazia com status 204

@router.get(
    "/unidade/{unidade}",
    response_model=List[processo_schemas.ProcessoRead],
    summary="Lista processos por unidade"
)
async def list_processos_by_unidade(
    unidade: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Lista processos por unidade."""
    logger.info(f"Recebida requisição para listar processos por unidade: {unidade}")
    repo = ProcessoRepository(db)
    processos = await repo.pesquisar_processos_por_unidade(unidade)
    logger.debug(f"Retornando {len(processos)} processos.")
    return processos
    