#!/usr/bin/env python3
"""
Script para comparar os modelos Python com o banco de dados
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey

# Define as variáveis de ambiente diretamente
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'admin'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5432'
os.environ['DB_NAME'] = 'postgres'
os.environ['DB_DATABASE'] = 'postgres'

def get_database_schema():
    """Obtém o schema atual do banco de dados"""
    print("=== SCHEMA DO BANCO DE DADOS ===")
    
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
        db_schema = {}
        
        for table in tables:
            if table in ['users_safs', 'itens_catalogo', 'planejamento_aquisicao']:
                print(f"\nTabela: {table}")
                columns = inspector.get_columns(table)
                db_schema[table] = columns
                
                for col in columns:
                    print(f"  - {col['name']}: {col['type']} (nullable={col['nullable']})")
                
                # Verifica foreign keys
                foreign_keys = inspector.get_foreign_keys(table)
                if foreign_keys:
                    print(f"  Foreign Keys:")
                    for fk in foreign_keys:
                        print(f"    - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        return db_schema
        
    except Exception as e:
        print(f"✗ Erro ao conectar com o banco: {e}")
        return None

def get_models_schema():
    """Obtém o schema dos modelos Python"""
    print("\n=== SCHEMA DOS MODELOS PYTHON ===")
    
    try:
        # Importa os modelos
        from app_catalogo.models.base import Base
        from app_catalogo.models.user import User
        from app_catalogo.models.catalogo import ItensCatalogo
        from app_catalogo.models.controle_processo import PlanejamentoAquisicao
        
        # Obtém o metadata
        metadata = Base.metadata
        models_schema = {}
        
        for table_name, table in metadata.tables.items():
            if table_name in ['users_safs', 'itens_catalogo', 'planejamento_aquisicao']:
                print(f"\nTabela: {table_name}")
                models_schema[table_name] = []
                
                for column in table.columns:
                    print(f"  - {column.name}: {column.type} (nullable={column.nullable})")
                    models_schema[table_name].append({
                        'name': column.name,
                        'type': str(column.type),
                        'nullable': column.nullable
                    })
                
                # Verifica foreign keys
                for fk in table.foreign_keys:
                    print(f"  Foreign Key: {fk.parent.name} -> {fk.column.table.name}.{fk.column.name}")
        
        return models_schema
        
    except Exception as e:
        print(f"✗ Erro ao importar modelos: {e}")
        return None

def compare_schemas(db_schema, models_schema):
    """Compara os schemas do banco e dos modelos"""
    print("\n=== COMPARAÇÃO DOS SCHEMAS ===")
    
    if not db_schema or not models_schema:
        print("❌ Não foi possível obter os schemas para comparação")
        return
    
    for table_name in ['users_safs', 'itens_catalogo', 'planejamento_aquisicao']:
        print(f"\n--- {table_name} ---")
        
        if table_name not in db_schema:
            print(f"❌ Tabela {table_name} não existe no banco")
            continue
            
        if table_name not in models_schema:
            print(f"❌ Tabela {table_name} não existe nos modelos")
            continue
        
        db_columns = {col['name']: col for col in db_schema[table_name]}
        model_columns = {col['name']: col for col in models_schema[table_name]}
        
        # Colunas que existem no banco mas não nos modelos
        db_only = set(db_columns.keys()) - set(model_columns.keys())
        if db_only:
            print(f"❌ Colunas apenas no banco: {list(db_only)}")
        
        # Colunas que existem nos modelos mas não no banco
        model_only = set(model_columns.keys()) - set(db_columns.keys())
        if model_only:
            print(f"❌ Colunas apenas nos modelos: {list(model_only)}")
        
        # Colunas comuns - verificar diferenças
        common_columns = set(db_columns.keys()) & set(model_columns.keys())
        for col_name in common_columns:
            db_col = db_columns[col_name]
            model_col = model_columns[col_name]
            
            if str(db_col['type']) != model_col['type'] or db_col['nullable'] != model_col['nullable']:
                print(f"⚠️  Diferença na coluna {col_name}:")
                print(f"   Banco: {db_col['type']} (nullable={db_col['nullable']})")
                print(f"   Modelo: {model_col['type']} (nullable={model_col['nullable']})")
        
        if not db_only and not model_only and not any(str(db_columns[col]['type']) != models_schema[table_name][i]['type'] or db_columns[col]['nullable'] != models_schema[table_name][i]['nullable'] for i, col in enumerate(common_columns)):
            print(f"✅ Tabela {table_name} está sincronizada")

if __name__ == "__main__":
    print("=== COMPARAÇÃO DE SCHEMAS ===")
    
    # Obtém o schema do banco
    db_schema = get_database_schema()
    
    # Obtém o schema dos modelos
    models_schema = get_models_schema()
    
    # Compara os schemas
    compare_schemas(db_schema, models_schema) 