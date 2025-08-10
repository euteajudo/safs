#!/usr/bin/env python3
"""
Script para corrigir a versão do Alembic no banco de dados
"""

import os
from sqlalchemy import create_engine, text

# Define as variáveis de ambiente
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'admin'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5432'
os.environ['DB_NAME'] = 'postgres'

def fix_alembic_version():
    """Corrige a versão do Alembic no banco"""
    print("=== CORRIGINDO VERSÃO DO ALEMBIC ===")
    
    try:
        # Conecta ao banco
        database_url = "postgresql://postgres:admin@localhost:5432/postgres"
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Verifica a versão atual
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            current_version = result.scalar()
            print(f"Versão atual no banco: {current_version}")
            
            # Atualiza para a versão correta
            conn.execute(text("UPDATE alembic_version SET version_num = '1dea829283ae'"))
            conn.commit()
            
            # Verifica se foi atualizada
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            new_version = result.scalar()
            print(f"Nova versão no banco: {new_version}")
            
            print("✅ Versão do Alembic corrigida com sucesso!")
            return True
            
    except Exception as e:
        print(f"✗ Erro ao corrigir versão: {e}")
        return False

if __name__ == "__main__":
    fix_alembic_version() 