#!/usr/bin/env python3
"""
Script para debugar o problema de login específico
"""

import asyncio
import sys
import os
import logging

# Adiciona o diretório backend ao path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Configurar logging para ver detalhes
logging.basicConfig(level=logging.DEBUG)

from app_catalogo.db_repository.conex_db import get_db
from app_catalogo.db_repository.user_repository import UserRepository
from app_catalogo.utils.security import verify_password, get_password_hash, create_access_token

async def debug_authentication():
    """Debug completo do processo de autenticação"""
    
    print("🔧 DEBUG: Iniciando debug completo de autenticação...\n")
    
    username = "teste2"
    password = "123456"
    
    try:
        async for db in get_db():
            print("✅ Conexão com banco estabelecida")
            
            # 1. Buscar usuário
            user_repo = UserRepository(db)
            print(f"🔍 Buscando usuário '{username}'...")
            user = await user_repo.pesquisar_por_username(username)
            
            if not user:
                print(f"❌ Usuário '{username}' não encontrado!")
                
                # Vamos listar todos os usuários disponíveis
                print("\n📋 Listando todos os usuários disponíveis:")
                all_users = await user_repo.listar_usuarios_paginados(limit=10)
                for u in all_users:
                    print(f"  - ID: {u.id}, Username: {u.username}, Email: {u.email}, Active: {u.is_active}")
                
                # Vamos criar o usuário de teste
                print(f"\n🔧 Criando usuário de teste '{username}'...")
                try:
                    user_data = {
                        "username": username,
                        "email": "teste2@example.com", 
                        "nome": "Usuário Teste 2",
                        "senha": password,  # Será hasheada automaticamente
                        "is_active": True
                    }
                    user = await user_repo.criar_usuario(user_data)
                    print(f"✅ Usuário criado: ID {user.id}")
                except Exception as create_error:
                    print(f"❌ Erro ao criar usuário: {create_error}")
                    return
            else:
                print(f"✅ Usuário encontrado: ID {user.id}, Active: {user.is_active}")
            
            # 2. Verificar senha
            print(f"\n🔍 Verificando senha para '{username}'...")
            print(f"  - Hash armazenado: {user.senha[:50]}...")
            
            is_password_valid = verify_password(password, user.senha)
            print(f"  - Senha válida: {is_password_valid}")
            
            if not is_password_valid:
                # Vamos testar gerando um novo hash
                print("🔧 Testando geração de novo hash...")
                new_hash = get_password_hash(password)
                print(f"  - Novo hash: {new_hash[:50]}...")
                
                # Verifica se o novo hash funciona
                test_verify = verify_password(password, new_hash)
                print(f"  - Novo hash válido: {test_verify}")
                
                # Atualiza a senha do usuário com o novo hash
                print("🔧 Atualizando senha do usuário...")
                try:
                    updated_user = await user_repo.atualizar_usuario(user.id, {"senha": password})
                    if updated_user:
                        print("✅ Senha atualizada com sucesso!")
                        user = updated_user
                        is_password_valid = True
                    else:
                        print("❌ Falha ao atualizar senha")
                except Exception as update_error:
                    print(f"❌ Erro ao atualizar senha: {update_error}")
            
            # 3. Verificar se usuário está ativo
            if not user.is_active:
                print(f"❌ Usuário '{username}' está inativo!")
                # Ativar usuário
                print("🔧 Ativando usuário...")
                try:
                    updated_user = await user_repo.atualizar_usuario(user.id, {"is_active": True})
                    if updated_user:
                        print("✅ Usuário ativado!")
                        user = updated_user
                    else:
                        print("❌ Falha ao ativar usuário")
                except Exception as activate_error:
                    print(f"❌ Erro ao ativar usuário: {activate_error}")
            
            # 4. Gerar token se tudo estiver OK
            if is_password_valid and user.is_active:
                print(f"\n🔑 Gerando token para '{username}'...")
                try:
                    access_token = create_access_token(data={"sub": user.username})
                    print(f"✅ Token gerado com sucesso!")
                    print(f"  - Token: {access_token[:50]}...")
                    
                    # Simula o retorno da API
                    response = {
                        "access_token": access_token,
                        "token_type": "bearer"
                    }
                    print(f"\n✅ Resposta da API seria: {response}")
                    
                except Exception as token_error:
                    print(f"❌ Erro ao gerar token: {token_error}")
            else:
                print(f"\n❌ Não é possível gerar token:")
                print(f"  - Senha válida: {is_password_valid}")
                print(f"  - Usuário ativo: {user.is_active if user else False}")
    
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_authentication())