#!/usr/bin/env python3
"""
Script para criar usuário de teste
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Adicionar o caminho do backend ao sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'backend'))

from app_catalogo.models.user import User
from app_catalogo.utils.security import get_password_hash
from app_catalogo.models.base import Base

# Configuração do banco de dados
DATABASE_URL = "sqlite+aiosqlite:///./backend/backend/catalogo.db"

async def create_test_user():
    """Cria usuário de teste"""
    # Criar engine e sessão
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            # Verificar se usuário já existe
            from sqlalchemy import select
            stmt = select(User).where(User.username == "teste")
            result = await session.execute(stmt)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print("✅ Usuário 'teste' já existe!")
                return
            
            # Criar novo usuário
            new_user = User(
                unidade="ULOG",
                nome="Usuário de Teste",
                username="teste",
                email="teste@example.com",
                senha=get_password_hash("teste123"),
                is_active=True,
                is_superuser=True,
                is_chefe_unidade=True,
                is_chefe_setor=True,
                is_funcionario=True
            )
            
            session.add(new_user)
            await session.commit()
            
            print("✅ Usuário de teste criado com sucesso!")
            print("   Username: teste")
            print("   Password: teste123")
            print("   Permissões: Todas (superuser)")
            
        except Exception as e:
            print(f"❌ Erro ao criar usuário: {e}")
            await session.rollback()
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_test_user())
