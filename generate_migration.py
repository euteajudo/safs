"""Script para gerar migration do Alembic"""
import subprocess
import os

# Navega para o diretório do backend
os.chdir(r"C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend")

# Executa o comando do alembic
try:
    result = subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", "adicionar_relacionamento_responsaveis_tecnicos"],
        capture_output=True,
        text=True,
        check=True
    )
    print("Output:", result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
except subprocess.CalledProcessError as e:
    print(f"Erro ao executar comando: {e}")
    print(f"Output: {e.stdout}")
    print(f"Error: {e.stderr}")