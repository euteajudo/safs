"""Rotas para responsáveis técnicos"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from sqlalchemy.exc import IntegrityError

from app_catalogo.models.resp_tec import ResponsavelTecnico
from app_catalogo.models.user import User
from app_catalogo.schemas import resp_tec as resp_tec_schemas
from app_catalogo.db_repository.conex_db import get_db
from app_catalogo.db_repository.op_db_resp_tec import ResponsavelTecnicoRepository
from app_catalogo.utils import security

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/responsaveis-tecnicos",
    tags=["Responsáveis Técnicos"],
    dependencies=[Depends(security.get_current_active_user)]
)

# --- MÉTODO POST ---

@router.post(
    "", 
    response_model=resp_tec_schemas.ResponsavelTecnicoRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo responsável técnico"
)
async def create_responsavel_tecnico(
    resp_tec_data: resp_tec_schemas.ResponsavelTecnicoCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Cria um novo responsável técnico."""
    logger.info(f"Usuário {current_user.email} tentando criar responsável técnico: {resp_tec_data.nome_res_tec}")
    repo = ResponsavelTecnicoRepository(db)
    try:
        novo_resp_tec = await repo.criar_responsavel_tecnico(resp_tec_data.model_dump())
        logger.info(f"Responsável técnico ID {novo_resp_tec.id} criado com sucesso.")
        return novo_resp_tec
    except IntegrityError:
        logger.warning(f"Falha ao criar responsável técnico. Nome '{resp_tec_data.nome_res_tec}' pode já existir.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Responsável técnico com nome '{resp_tec_data.nome_res_tec}' pode já existir.",
        )

# --- MÉTODOS GET ---

@router.get(
    "", 
    response_model=List[resp_tec_schemas.ResponsavelTecnicoRead],
    summary="Lista todos os responsáveis técnicos"
)
async def list_responsaveis_tecnicos(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    """Retorna uma lista paginada de todos os responsáveis técnicos."""
    repo = ResponsavelTecnicoRepository(db)
    responsaveis_tecnicos = await repo.listar_responsaveis_tecnicos_paginados(skip=skip, limit=limit)
    return responsaveis_tecnicos

@router.get(
    "/{resp_tec_id}", 
    response_model=resp_tec_schemas.ResponsavelTecnicoRead,
    summary="Busca um responsável técnico por seu ID"
)
async def get_responsavel_tecnico_by_id(
    resp_tec_id: int, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Retorna os detalhes de um responsável técnico específico pelo seu ID."""
    repo = ResponsavelTecnicoRepository(db)
    resp_tec = await repo.pesquisar_responsavel_tecnico_por_id(resp_tec_id)
    if resp_tec is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Responsável técnico não encontrado")
    return resp_tec

@router.get(
    "/nome/{nome}", 
    response_model=resp_tec_schemas.ResponsavelTecnicoRead,
    summary="Busca um responsável técnico pelo seu nome"
)
async def get_responsavel_tecnico_by_nome(
    nome: str, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Retorna os detalhes de um responsável técnico pelo seu nome."""
    repo = ResponsavelTecnicoRepository(db)
    resp_tec = await repo.pesquisar_responsavel_tecnico_por_nome(nome)
    if resp_tec is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Responsável técnico não encontrado")
    return resp_tec

# --- MÉTODO PATCH ---

@router.patch(
    "/{resp_tec_id}", 
    response_model=resp_tec_schemas.ResponsavelTecnicoRead,
    status_code=status.HTTP_200_OK,
    summary="Atualiza um responsável técnico"
)
async def update_responsavel_tecnico(
    resp_tec_id: int,
    resp_tec_data: resp_tec_schemas.ResponsavelTecnicoUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Atualiza parcialmente os dados de um responsável técnico."""
    logger.info(f"Usuário {current_user.email} atualizando responsável técnico ID {resp_tec_id}")
    
    repo = ResponsavelTecnicoRepository(db)
    resp_tec = await repo.pesquisar_responsavel_tecnico_por_id(resp_tec_id)
    
    if not resp_tec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Responsável técnico não encontrado"
        )
    
    # Atualiza o responsável técnico
    resp_tec_atualizado = await repo.atualizar_responsavel_tecnico(resp_tec_id, resp_tec_data.model_dump(exclude_unset=True))
    
    if not resp_tec_atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Falha ao atualizar responsável técnico"
        )
    
    logger.info(f"Responsável técnico ID {resp_tec_id} atualizado com sucesso")
    return resp_tec_atualizado

# --- MÉTODO DELETE ---

@router.delete(
    "/{resp_tec_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um responsável técnico"
)
async def delete_responsavel_tecnico(
    resp_tec_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(security.get_current_active_user)]
):
    """Remove um responsável técnico (requer permissão especial)."""
    if not (current_user.is_superuser or current_user.is_chefe_unidade or current_user.is_chefe_setor):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Apenas superusuários, chefes de unidade ou chefes de setor podem remover responsáveis técnicos"
        )
    
    logger.info(f"Usuário {current_user.email} tentando remover o responsável técnico ID {resp_tec_id}")
    repo = ResponsavelTecnicoRepository(db)
    success = await repo.deletar_responsavel_tecnico(resp_tec_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Responsável técnico não encontrado para remoção"
        )
    return None