#!/usr/bin/env python3
"""
Script de teste para verificar a autenticação do backend
"""

import asyncio
import sys
import os

# Adiciona o diretório backend ao path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app_catalogo.db_repository.conex_db import get_db
from app_catalogo.db_repository.user_repository import UserRepository
from app_catalogo.utils.security import verify_password, get_password_hash

async def test_database_connection():
    """Testa a conexão com o banco de dados"""
    print("🔍 Testando conexão com o banco de dados...")
    try:
        async for db in get_db():
            user_repo = UserRepository(db)
            users = await user_repo.listar_usuarios_paginados(limit=5)
            print(f"✅ Conexão OK! Encontrados {len(users)} usuários no banco")
            
            for user in users:
                print(f"  - User ID: {user.id}, Username: {user.username}, Email: {user.email}, Active: {user.is_active}")
            
            return users
    except Exception as e:
        print(f"❌ Erro na conexão com o banco: {e}")
        return None

async def test_specific_user(username="teste2"):
    """Testa se o usuário específico existe"""
    print(f"\n🔍 Verificando usuário '{username}'...")
    try:
        async for db in get_db():
            user_repo = UserRepository(db)
            user = await user_repo.pesquisar_por_username(username)
            
            if user:
                print(f"✅ Usuário encontrado:")
                print(f"  - ID: {user.id}")
                print(f"  - Username: {user.username}")
                print(f"  - Email: {user.email}")
                print(f"  - Active: {user.is_active}")
                print(f"  - Created: {user.created_at}")
                return user
            else:
                print(f"❌ Usuário '{username}' não encontrado!")
                return None
    except Exception as e:
        print(f"❌ Erro ao buscar usuário: {e}")
        return None

async def test_password_verification(username="teste2", password="123456"):
    """Testa a verificação de senha"""
    print(f"\n🔍 Testando senha para '{username}'...")
    try:
        async for db in get_db():
            user_repo = UserRepository(db)
            user = await user_repo.pesquisar_por_username(username)
            
            if not user:
                print(f"❌ Usuário '{username}' não encontrado!")
                return False
            
            # Testa a verificação da senha
            is_valid = verify_password(password, user.senha)
            if is_valid:
                print(f"✅ Senha correta para '{username}'!")
                return True
            else:
                print(f"❌ Senha incorreta para '{username}'!")
                print(f"  - Hash armazenado: {user.senha[:50]}...")
                # Vamos testar criando um novo hash da senha para comparar
                new_hash = get_password_hash(password)
                print(f"  - Novo hash gerado: {new_hash[:50]}...")
                return False
    except Exception as e:
        print(f"❌ Erro ao verificar senha: {e}")
        return False

async def create_test_user_if_needed():
    """Cria o usuário de teste se não existir"""
    print(f"\n🔧 Verificando se precisa criar usuário de teste...")
    try:
        async for db in get_db():
            user_repo = UserRepository(db)
            
            # Verifica se o usuário já existe
            existing_user = await user_repo.pesquisar_por_username("teste2")
            if existing_user:
                print("✅ Usuário 'teste2' já existe!")
                return existing_user
            
            # Cria o usuário de teste
            user_data = {
                "username": "teste2",
                "email": "teste2@example.com",
                "nome": "Usuário Teste 2",
                "senha": "123456",  # Será hasheada pelo repositório
                "is_active": True
            }
            
            new_user = await user_repo.criar_usuario(user_data)
            print(f"✅ Usuário de teste criado: {new_user.username}")
            return new_user
            
    except Exception as e:
        print(f"❌ Erro ao criar usuário de teste: {e}")
        return None

async def main():
    print("🚀 Iniciando testes de autenticação...\n")
    
    # Teste 1: Conexão com banco
    users = await test_database_connection()
    if not users:
        print("❌ Falha na conexão com banco. Abortando testes.")
        return
    
    # Teste 2: Verificar usuário específico
    user = await test_specific_user("teste2")
    
    # Teste 3: Criar usuário se não existir
    if not user:
        user = await create_test_user_if_needed()
    
    # Teste 4: Verificar senha
    if user:
        await test_password_verification("teste2", "123456")
    
    print("\n✅ Testes concluídos!")

if __name__ == "__main__":
    asyncio.run(main())