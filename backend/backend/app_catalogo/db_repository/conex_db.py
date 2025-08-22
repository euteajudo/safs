"""Conexão com o banco de dados"""

"""
Módulo para gerenciar conexões assíncronas com PostgreSQL usando SQLAlchemy.
Inclui pool de conexões e logging estruturado para uso com FastAPI.
Esse módulo é compatível com uma grande quantidade de conexões simultâneas.
Usei o SQLAlchemy porque é o mais rápido e eficiente para conexões assíncronas.
Usei context managers para garantir que as conexões sejam fechadas corretamente.
O arquivo possui vários pontos de log para debug.
"""

import os
import logging
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from contextlib import asynccontextmanager
from typing import AsyncGenerator

# Garante que o diretório de logs exista
os.makedirs("logs", exist_ok=True)

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename="logs/db_conex.log",
    filemode="a",
)
logger = logging.getLogger("database_orm")

load_dotenv()

# Pegar valores do ambiente com defaults
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'postgres')

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Criação do engine com pooling e logging de eventos principais
try:
    logger.info("Inicializando engine SQLAlchemy...")
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,  # Mude para True se quiser log detalhado de queries
        pool_size=10, # Ajuste de acordo com a quantidade de conexões necessárias
        max_overflow=20, # Aqui você pode ajustar o número máximo de conexões extras
        pool_timeout=30, # Tempo limite para obter uma conexão do pool
        pool_recycle=1800, # Recicla as conexões após 1800 segundos (30 minutos). Ajuste de acordo com a sua necessidade.
    )
    logger.info("Engine SQLAlchemy inicializado com sucesso.")
except Exception as exc:
    logger.critical("Erro ao inicializar engine SQLAlchemy: %s", exc)
    raise

# Sessionmaker async (ORM)
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def get_db_session() -> AsyncGenerator:
    """
    Context manager para sessão ORM async.
    Garante abertura, fechamento e logging de sessão.
    Uso:
        async with get_db_session() as session:
            await session.execute(...)
    """
    session = None
    try:
        logger.debug("Abrindo nova sessão ORM SQLAlchemy...")
        session = AsyncSessionLocal()
        yield session
        logger.debug("Sessão ORM concluída com sucesso.")
    except Exception as exc:
        logger.error("Erro durante operação com sessão ORM: %s", exc)
        if session:
            await session.rollback()
        raise
    finally:
        if session:
            await session.close()
            logger.debug("Sessão ORM fechada.")

# Dependência para o FastAPI
async def get_db():
    """
    Dependência do FastAPI para obter sessão do banco de dados.
    """
    session = AsyncSessionLocal()
    try:
        logger.debug("Sessão ORM criada para requisição FastAPI")
        yield session
    except Exception as exc:
        logger.error("Erro durante operação com sessão ORM: %s", exc)
        await session.rollback()
        raise
    finally:
        await session.close()
        logger.debug("Sessão ORM fechada após requisição FastAPI")