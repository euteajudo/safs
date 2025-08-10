#!/usr/bin/env python3
"""
Script para fazer stamp do banco de dados existente no Alembic
Isso sincroniza o Alembic com o estado atual do banco sem fazer alterações
"""

import os
import sys
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text, inspect

# Define as variáveis de ambiente diretamente
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'admin'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5432'
os.environ['DB_NAME'] = 'postgres'
os.environ['DB_DATABASE'] = 'postgres'

def check_current_state():
    """Verifica o estado atual antes do stamp"""
    print("=== ESTADO ATUAL ANTES DO STAMP ===")
    
    # Configuração da conexão
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    print(f"Tentando conectar com: {database_url}")
    
    try:
        engine = create_engine(database_url)
        inspector = inspect(engine)
        
        # Verifica se a tabela alembic_version existe
        tables = inspector.get_table_names()
        print(f"Tabelas no banco: {tables}")
        
        if 'alembic_version' in tables:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT version_num FROM alembic_version"))
                version = result.scalar()
                print(f"Versão atual no banco: {version}")
        else:
            print("Tabela alembic_version não existe - será criada pelo stamp")
            
        # Verifica as tabelas de aplicação
        app_tables = ['users_safs', 'itens_catalogo', 'planejamento_aquisicao']
        for table in app_tables:
            if table in tables:
                print(f"✓ Tabela {table} existe")
                columns = inspector.get_columns(table)
                print(f"  Colunas: {[col['name'] for col in columns]}")
            else:
                print(f"✗ Tabela {table} não existe")
                
    except Exception as e:
        print(f"✗ Erro ao conectar com o banco: {e}")
        return False
    
    return True

def stamp_database():
    """Faz o stamp do banco de dados"""
    print("\n=== FAZENDO STAMP DO BANCO ===")
    
    try:
        config = Config('alembic.ini')
        
        # Primeiro, vamos verificar qual é a última revisão disponível
        from alembic.script import ScriptDirectory
        script_dir = ScriptDirectory.from_config(config)
        heads = script_dir.get_heads()
        
        if heads:
            latest_revision = heads[0]
            print(f"Última revisão disponível: {latest_revision}")
            
            # Faz o stamp para a última revisão
            print("Executando stamp...")
            command.stamp(config, latest_revision)
            print("✓ Stamp concluído com sucesso!")
            
            # Verifica o estado após o stamp
            print("\n=== ESTADO APÓS O STAMP ===")
            command.current(config)
            
        else:
            print("✗ Nenhuma revisão encontrada")
            return False
            
    except Exception as e:
        print(f"✗ Erro durante o stamp: {e}")
        return False
    
    return True

def verify_stamp():
    """Verifica se o stamp foi bem-sucedido"""
    print("\n=== VERIFICAÇÃO PÓS-STAMP ===")
    
    try:
        config = Config('alembic.ini')
        
        # Verifica o status atual
        print("Status atual do Alembic:")
        command.current(config)
        
        # Verifica se há diferenças entre o banco e os modelos
        print("\nVerificando diferenças...")
        command.check(config)
        print("✓ Nenhuma diferença encontrada - banco sincronizado!")
        
    except Exception as e:
        print(f"✗ Erro na verificação: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=== SCRIPT DE STAMP DO ALEMBIC ===")
    print("Este script irá sincronizar o Alembic com o estado atual do banco")
    print("SEM fazer alterações no banco de dados.\n")
    
    # Verifica o estado atual
    if not check_current_state():
        print("❌ Não foi possível verificar o estado atual. Abortando.")
        sys.exit(1)
    
    # Faz o stamp
    if not stamp_database():
        print("❌ Erro durante o stamp. Abortando.")
        sys.exit(1)
    
    # Verifica o resultado
    if not verify_stamp():
        print("❌ Erro na verificação pós-stamp.")
        sys.exit(1)
    
    print("\n🎉 STAMP CONCLUÍDO COM SUCESSO!")
    print("O Alembic agora está sincronizado com o estado atual do banco de dados.")
    print("Você pode usar 'alembic revision --autogenerate' para gerar novas migrações baseadas em mudanças futuras nos modelos.") 