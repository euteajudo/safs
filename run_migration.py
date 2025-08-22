"""Script para executar migrations do Alembic"""
import subprocess
import os

# Navega para o diretório do backend
os.chdir(r"C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend")

print("Executando migrations do Alembic...")
print("-" * 50)

# Executa o comando do alembic upgrade
try:
    # Primeiro, mostra o status atual
    print("Status atual das migrations:")
    result = subprocess.run(
        ["alembic", "current"],
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)
    
    # Executa as migrations pendentes
    print("\nExecutando migrations pendentes...")
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
        check=True
    )
    print("Output:", result.stdout)
    if result.stderr:
        print("Avisos:", result.stderr)
    
    print("\nMigrations executadas com sucesso!")
    
except subprocess.CalledProcessError as e:
    print(f"Erro ao executar comando: {e}")
    print(f"Output: {e.stdout}")
    print(f"Error: {e.stderr}")
    print("\nSe houver erro de tabela já existente, você pode executar:")
    print("  alembic stamp head  # Para marcar todas as migrations como executadas")
    print("ou")
    print("  alembic downgrade -1  # Para reverter a última migration")