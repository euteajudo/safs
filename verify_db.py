import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
cur = conn.cursor()

# Verificar estrutura das tabelas
print('=== ESTRUTURA DAS TABELAS ===')
tables = ['users_safs', 'itens_catalogo', 'planejamento_aquisicao', 'item_processo']

for table in tables:
    print(f'\n📋 Tabela: {table}')
    cur.execute(f"""
        SELECT column_name, data_type, is_nullable, column_default 
        FROM information_schema.columns 
        WHERE table_name = '{table}' 
        ORDER BY ordinal_position;
    """)
    columns = cur.fetchall()
    for col in columns:
        nullable = '✅' if col[2] == 'YES' else '❌'
        print(f'  • {col[0]} ({col[1]}) - Nullable: {nullable}')

cur.close()
conn.close()
print('\n🎉 Verificação concluída com sucesso!')
