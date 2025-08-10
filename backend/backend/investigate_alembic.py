#!/usr/bin/env python3
"""
Script para investigar o estado do Alembic e do banco de dados
"""

import os
import sys
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def check_alembic_status():
    """Verifica o status atual do Alembic"""
    print("=== STATUS DO ALEMBIC ===")
    try:
        config = Config('alembic.ini')
        command.current(config)
        print("✓ Alembic configurado corretamente")
    except Exception as e:
        print(f"✗ Erro no Alembic: {e}")

def check_database_tables():
    """Verifica as tabelas existentes no banco de dados"""
    print("\n=== TABELAS NO BANCO DE DADOS ===")
    
    # Configuração da conexão
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    try:
        engine = create_engine(database_url)
        inspector = inspect(engine)
        
        tables = inspector.get_table_names()
        print(f"Tabelas encontradas: {tables}")
        
        # Verifica se as tabelas esperadas existem
        expected_tables = ['users_safs', 'itens_catalogo', 'planejamento_aquisicao']
        for table in expected_tables:
            if table in tables:
                print(f"✓ Tabela {table} existe")
                
                # Verifica as colunas
                columns = inspector.get_columns(table)
                print(f"  Colunas em {table}: {[col['name'] for col in columns]}")
                
                # Verifica as foreign keys
                foreign_keys = inspector.get_foreign_keys(table)
                if foreign_keys:
                    print(f"  Foreign keys em {table}: {foreign_keys}")
            else:
                print(f"✗ Tabela {table} NÃO existe")
                
    except Exception as e:
        print(f"✗ Erro ao conectar com o banco: {e}")

def check_alembic_version_table():
    """Verifica a tabela alembic_version"""
    print("\n=== TABELA ALEMBIC_VERSION ===")
    
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            version = result.scalar()
            print(f"Versão atual no banco: {version}")
            
            # Lista todas as versões
            result = conn.execute(text("SELECT * FROM alembic_version"))
            versions = result.fetchall()
            print(f"Todas as versões: {versions}")
            
    except Exception as e:
        print(f"✗ Erro ao verificar alembic_version: {e}")

def check_models():
    """Verifica se os modelos podem ser importados corretamente"""
    print("\n=== VERIFICAÇÃO DOS MODELOS ===")
    
    try:
        from app_catalogo.models.base import Base
        from app_catalogo.models.user import User
        from app_catalogo.models.catalogo import ItensCatalogo
        from app_catalogo.models.controle_processo import PlanejamentoAquisicao
        
        print("✓ Todos os modelos importados com sucesso")
        print(f"✓ Base metadata: {Base.metadata}")
        
        # Lista as tabelas definidas nos modelos
        tables = Base.metadata.tables.keys()
        print(f"Tabelas definidas nos modelos: {list(tables)}")
        
    except Exception as e:
        print(f"✗ Erro ao importar modelos: {e}")

if __name__ == "__main__":
    check_alembic_status()
    check_database_tables()
    check_alembic_version_table()
    check_models() 