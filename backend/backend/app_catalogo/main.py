"""Arquivo principal da API"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app_catalogo.routers import login, users, catalogo, controle_processos, resp_tec

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- CRIAÇÃO DA APLICAÇÃO FASTAPI ---

app = FastAPI(
    title="API Catálogo de Processos",
    description="""
    API para gerenciamento do catálogo de itens e processos de aquisição.
    
    ## Autenticação
    Para usar os endpoints protegidos, você precisa:
    1. Fazer login em `/api/v1/token` com username e password
    2. Usar o token retornado no header Authorization: Bearer {token}
    
    ## Usuário de Teste
    - Username: `teste2`
    - Password: `123456`
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Login",
            "description": "Operações de autenticação e login"
        },
        {
            "name": "Usuários",
            "description": "Operações de gerenciamento de usuários"
        },
        {
            "name": "Processos de Aquisição",
            "description": "Operações de gerenciamento de processos de aquisição"
        },
        {
            "name": "Catálogo de Itens",
            "description": "Operações de gerenciamento do catálogo de itens"
        },
        {
            "name": "Responsáveis Técnicos",
            "description": "Operações de gerenciamento de responsáveis técnicos"
        },
        {
            "name": "Health Check",
            "description": "Verificação de status da API"
        }
    ]
)

# --- CONFIGURAÇÃO DO CORS (Cross-Origin Resource Sharing) ---

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:3002",
    "http://127.0.0.1:3002",
    "http://localhost:8080",  # Common dev port
    "http://127.0.0.1:8080",
    "http://10.28.130.20:3000",  # Network address from Next.js output
    "http://10.28.130.20:3001",
    "http://10.28.130.20:3002",
    "*",  # Allow all origins for debugging (remove in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix="/api/v1", tags=["Login"])

app.include_router(users.router, prefix="/api/v1/users", tags=["Usuários"])
app.include_router(controle_processos.router, prefix="/api/v1/processos", tags=["Processos de Aquisição"])
app.include_router(catalogo.router, prefix="/api/v1/catalogo", tags=["Catálogo de Itens"])
app.include_router(resp_tec.router, prefix="/api/v1", tags=["Responsáveis Técnicos"])


@app.get("/api/v1/health", tags=["Health Check"])
async def health_check():
    """
    Endpoint de verificação de saúde. Retorna uma mensagem de sucesso
    se a API estiver funcionando.
    """
    return {"status": "ok", "message": "API do Catálogo de Processos está no ar!"}

@app.get("/api/v1/test-auth", tags=["Health Check"])
async def test_auth():
    """
    Endpoint de teste que não requer autenticação.
    """
    return {"message": "Este endpoint não requer autenticação!"}

@app.post("/api/v1/login-simple", tags=["Health Check"])
async def login_simple(username: str, password: str):
    """
    Endpoint de login simplificado para teste.
    Use este endpoint para obter um token de acesso.
    """
    from app_catalogo.db_repository.user_repository import UserRepository
    from app_catalogo.db_repository.conex_db import get_db
    from app_catalogo.utils import security
    
    async for db in get_db():
        user_repo = UserRepository(db)
        user = await user_repo.pesquisar_por_username(username=username)
        
        if not user or not security.verify_password(password, user.senha):
            raise HTTPException(
                status_code=401,
                detail="Username ou senha incorretos"
            )
        
        access_token = security.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}









