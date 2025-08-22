
"""
Configuração do Alembic para os modelos do banco de dados
"""

import os
import sys
from sqlalchemy import pool
from alembic import context
from logging.config import fileConfig
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar os modelos SQLAlchemy
from app_catalogo.models.base import Base
from app_catalogo.models.user import User
from app_catalogo.models.catalogo import ItensCatalogo
from app_catalogo.models.controle_processo import PlanejamentoAquisicao
from app_catalogo.models.resp_tec import ResponsavelTecnico




# Carrega as variáveis de ambiente
# Força recarregamento e ignora variáveis do sistema
env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')
print(f"Procurando arquivo .env em: {env_file_path}")
print(f"Arquivo .env existe: {os.path.exists(env_file_path)}")

# Força recarregamento do .env e sobrescreve variáveis do sistema
load_dotenv(env_file_path, override=True)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Validação das variáveis de ambiente
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
# Tenta DB_NAME primeiro, depois DB_DATABASE como fallback
db_name = os.getenv('DB_NAME') or os.getenv('DB_DATABASE')

print("Variáveis de ambiente:")
print(f"DB_USER: {db_user}")
print(f"DB_PASSWORD: {'*' * len(db_password) if db_password else 'None'}")
print(f"DB_HOST: {db_host}")
print(f"DB_PORT: {db_port}")
print(f"DB_NAME: {db_name}")

# Debug: Mostra todas as variáveis de ambiente que começam com DB_
print("\nTodas as variáveis DB_ encontradas:")
for key, value in os.environ.items():
    if key.startswith('DB_'):
        if 'PASSWORD' in key:
            print(f"{key}: {'*' * len(value) if value else 'None'}")
        else:
            print(f"{key}: {value}")

# Verifica se todas as variáveis estão definidas
if not all([db_user, db_password, db_host, db_port, db_name]):
    raise ValueError("Todas as variáveis de ambiente do banco de dados devem estar definidas: DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME")

# Tenta resolver o hostname para IP se necessário
import socket
from urllib.parse import quote_plus

try:
    resolved_ip = socket.gethostbyname(db_host)
    print(f"Hostname {db_host} resolvido para IP: {resolved_ip}")
    # Usa o IP resolvido ao invés do hostname
    db_host = resolved_ip
except socket.gaierror as e:
    print(f"Erro ao resolver hostname {db_host}: {e}")
    print("Tentando usar hostname original...")

# Codifica a senha para evitar problemas de caracteres especiais
encoded_password = quote_plus(db_password)

# Configura a URL do banco de dados usando as variáveis de ambiente
# Usa psycopg2 (síncrono) que é mais estável para migrações
database_url = f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
print("ALEMBIC DATABASE URL:", database_url)

# Não usa set_main_option para evitar problemas com caracteres especiais
# A URL será passada diretamente para o engine

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# Definir o target_metadata como o MetaData dos modelos SQLAlchemy
target_metadata = Base.metadata





# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection, target_metadata=target_metadata
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    from sqlalchemy import create_engine
    
    # Configurações para conexão síncrona
    engine_config = {
        "poolclass": pool.NullPool,
        "echo": False,
        "connect_args": {
            "application_name": "alembic_migration"
        }
    }
    
    # Se estiver usando IP, desabilita SSL
    if db_host.replace('.', '').isdigit():
        engine_config["connect_args"]["sslmode"] = "disable"
        print(f"Usando IP {db_host} - SSL desabilitado")
    
    # Usa a URL diretamente ao invés de config.get_main_option
    connectable = create_engine(
        database_url,
        **engine_config
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
