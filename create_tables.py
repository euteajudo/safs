#!/usr/bin/env python3
"""
Script para criar todas as tabelas do SAFS no PostgreSQL
"""

import os
import sys

# Adicionar o diretório backend ao path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'backend')
sys.path.insert(0, backend_dir)

from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carregar variáveis de ambiente
env_path = os.path.join(backend_dir, '.env')
load_dotenv(env_path)

# Importar todos os modelos
from app_catalogo.models.base import Base
from app_catalogo.models.user import User
from app_catalogo.models.catalogo import ItensCatalogo
from app_catalogo.models.controle_processo import PlanejamentoAquisicao
from app_catalogo.models.resp_tec import ResponsavelTecnico

def create_all_tables():
    """Criar todas as tabelas no banco de dados"""
    
    # Configurar URL de conexão
    database_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    
    print(f"Conectando ao banco: {database_url}")
    
    # Criar engine
    engine = create_engine(
        database_url,
        echo=True  # Para ver os SQLs executados
    )
    
    try:
        # Criar todas as tabelas
        print("Criando todas as tabelas...")
        Base.metadata.create_all(engine)
        print("✅ Todas as tabelas foram criadas com sucesso!")
        
        # Verificar tabelas criadas
        print("\nTabelas criadas:")
        with engine.connect() as conn:
            result = conn.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            for row in result:
                print(f"  - {row[0]}")
                
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = create_all_tables()
    sys.exit(0 if success else 1)