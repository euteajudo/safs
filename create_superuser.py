#!/usr/bin/env python3
"""
Script para criar um superusuário no sistema SAFS
"""

import os
import sys
from datetime import datetime, timezone

# Adicionar o diretório backend ao path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'backend')
sys.path.insert(0, backend_dir)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from passlib.context import CryptContext

# Carregar variáveis de ambiente
env_path = os.path.join(backend_dir, '.env')
load_dotenv(env_path)

# Configurar criptografia de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Gerar hash da senha usando bcrypt"""
    return pwd_context.hash(password)

def create_superuser():
    """Criar um superusuário no banco de dados"""
    
    # Configurar URL de conexão
    database_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    
    print(f"Conectando ao banco: {database_url}")
    
    # Criar engine e sessão
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    try:
        with SessionLocal() as session:
            # Dados do superusuário
            superuser_data = {
                'unidade': 'SAFS',
                'nome': 'Administrador do Sistema',
                'username': 'admin',
                'email': 'admin@safs.gov.br',
                'senha': hash_password('admin123'),  # Senha: admin123
                'foto_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face',
                'is_active': True,
                'is_superuser': True,
                'is_chefe_unidade': True,
                'is_chefe_setor': False,
                'is_funcionario': False,
                'created_at': datetime.now(timezone.utc).replace(tzinfo=None),
                'updated_at': datetime.now(timezone.utc).replace(tzinfo=None)
            }
            
            # Verificar se o usuário já existe
            check_query = text("SELECT id FROM users_safs WHERE username = :username OR email = :email")
            existing_user = session.execute(check_query, {
                'username': superuser_data['username'],
                'email': superuser_data['email']
            }).fetchone()
            
            if existing_user:
                print(f"❌ Usuário já existe com username '{superuser_data['username']}' ou email '{superuser_data['email']}'")
                return False
            
            # Inserir o superusuário
            insert_query = text("""
                INSERT INTO users_safs (
                    unidade, nome, username, email, senha, foto_url,
                    is_active, is_superuser, is_chefe_unidade, is_chefe_setor, is_funcionario,
                    created_at, updated_at
                ) VALUES (
                    :unidade, :nome, :username, :email, :senha, :foto_url,
                    :is_active, :is_superuser, :is_chefe_unidade, :is_chefe_setor, :is_funcionario,
                    :created_at, :updated_at
                )
            """)
            
            session.execute(insert_query, superuser_data)
            session.commit()
            
            print("✅ Superusuário criado com sucesso!")
            print(f"📧 Email: {superuser_data['email']}")
            print(f"👤 Username: {superuser_data['username']}")
            print(f"🔑 Senha: admin123")
            print(f"🏢 Unidade: {superuser_data['unidade']}")
            print(f"⚡ Permissões: Superusuário + Chefe de Unidade")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {e}")
        return False

def verify_superuser():
    """Verificar se o superusuário foi criado corretamente"""
    
    database_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    try:
        with SessionLocal() as session:
            query = text("""
                SELECT id, nome, username, email, unidade, is_superuser, is_chefe_unidade, is_active
                FROM users_safs 
                WHERE username = 'admin'
            """)
            
            user = session.execute(query).fetchone()
            
            if user:
                print("\n📋 Verificação do Superusuário:")
                print(f"   ID: {user[0]}")
                print(f"   Nome: {user[1]}")
                print(f"   Username: {user[2]}")
                print(f"   Email: {user[3]}")
                print(f"   Unidade: {user[4]}")
                print(f"   Superusuário: {'✅' if user[5] else '❌'}")
                print(f"   Chefe Unidade: {'✅' if user[6] else '❌'}")
                print(f"   Ativo: {'✅' if user[7] else '❌'}")
                return True
            else:
                print("❌ Superusuário não encontrado!")
                return False
                
    except Exception as e:
        print(f"❌ Erro ao verificar superusuário: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Criando superusuário para o sistema SAFS...")
    
    if create_superuser():
        verify_superuser()
        print("\n🎉 Pronto! Você pode fazer login no sistema com as credenciais acima.")
    else:
        print("\n💥 Falha ao criar superusuário.")
        sys.exit(1)