
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

# Importa os módulos que criamos
from app_catalogo.schemas.token_data import Token
from app_catalogo.db_repository.conex_db import get_db
from app_catalogo.db_repository.user_repository import UserRepository
from app_catalogo.utils import security





# Cria um novo roteador para organizar as rotas de login
router = APIRouter(
    tags=["Login"]
)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    # Annotated é a forma moderna de usar Depends
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Endpoint para autenticar um usuário e retornar um token de acesso JWT.
    
    Recebe 'username' e 'password' via form data.
    """
    # 1. Busca o usuário pelo username
    user_repo = UserRepository(db)
    user = await user_repo.pesquisar_por_username(username=form_data.username)

    # 2. Verifica se o usuário existe e se a senha está correta
    if not user or not security.verify_password(form_data.password, user.senha):
        # Se a autenticação falhar, levanta um erro HTTP 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Se a autenticação for bem-sucedida, cria o token
    # O 'sub' (subject) do token será o username do usuário
    access_token = security.create_access_token(
        data={"sub": user.username}
    )

    # 4. Preparar dados do usuário para retorno
    from app_catalogo.schemas.token_data import UserInToken
    user_data = UserInToken(
        id=user.id,
        username=user.username,
        nome=user.nome,
        email=user.email,
        unidade=user.unidade,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        is_chefe_unidade=user.is_chefe_unidade,
        is_chefe_setor=user.is_chefe_setor,
        is_funcionario=user.is_funcionario,
        foto_url=getattr(user, 'foto_url', None),
        created_at=user.created_at,
        updated_at=getattr(user, 'updated_at', None)
    )

    # 5. Retorna o token e dados do usuário para o cliente
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user_data
    }