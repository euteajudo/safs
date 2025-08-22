"""
Script para executar migrations do Alembic no Windows
"""
import os
import sys
import subprocess
from pathlib import Path

# Adiciona o diretório do backend ao PATH
backend_dir = Path(r"C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend")
sys.path.insert(0, str(backend_dir))
os.chdir(backend_dir)

def run_command(cmd):
    """Executa um comando e mostra o resultado"""
    print(f"\n>>> Executando: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        # Usa o Python do venv se existir
        venv_python = backend_dir / "venv" / "Scripts" / "python.exe"
        if venv_python.exists():
            # Se estamos usando venv, usa o alembic do venv
            if cmd[0] == "alembic":
                alembic_path = backend_dir / "venv" / "Scripts" / "alembic.exe"
                if alembic_path.exists():
                    cmd[0] = str(alembic_path)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=backend_dir,
            shell=True
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Avisos/Erros: {result.stderr}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return False

def main():
    print("=" * 60)
    print("EXECUTANDO MIGRATIONS DO ALEMBIC")
    print("=" * 60)
    
    # Verifica se o alembic está instalado
    print("\n1. Verificando instalação do Alembic...")
    if not run_command(["pip", "show", "alembic"]):
        print("Alembic não encontrado. Instalando...")
        run_command(["pip", "install", "alembic"])
    
    # Mostra o status atual
    print("\n2. Status atual das migrations:")
    run_command(["alembic", "current"])
    
    # Mostra o histórico
    print("\n3. Histórico de migrations:")
    run_command(["alembic", "history", "--verbose"])
    
    # Executa as migrations pendentes
    print("\n4. Aplicando migrations pendentes...")
    success = run_command(["alembic", "upgrade", "head"])
    
    if success:
        print("\n✅ Migrations executadas com sucesso!")
        
        # Mostra o novo status
        print("\n5. Novo status das migrations:")
        run_command(["alembic", "current"])
        
        print("\n✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("\nAs seguintes tabelas devem ter sido criadas/atualizadas:")
        print("  - responsavel_tecnico_item (nova)")
        print("  - item_processo (nova)")
        print("  - comprador_processo (se não existia)")
        print("  - comprador_item (se não existia)")
        print("  - controlador_item (se não existia)")
        
    else:
        print("\n❌ Erro ao executar migrations!")
        print("\nPossíveis soluções:")
        print("1. Verifique se o PostgreSQL está rodando")
        print("2. Verifique as credenciais no arquivo .env")
        print("3. Se as tabelas já existem, execute:")
        print("   alembic stamp head")
        print("4. Para reverter a última migration:")
        print("   alembic downgrade -1")

if __name__ == "__main__":
    main()
    input("\nPressione ENTER para fechar...")