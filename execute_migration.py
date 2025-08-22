#!/usr/bin/env python3

import os
import sys
import subprocess

def main():
    # Navegar para o diretório backend
    backend_dir = r"C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
    os.chdir(backend_dir)
    
    print(f"Diretório atual: {os.getcwd()}")
    
    try:
        # Primeiro, vamos ver o status atual
        print("=" * 50)
        print("1. Verificando status atual das migrations:")
        cmd_current = [sys.executable, "-m", "alembic", "current"]
        result = subprocess.run(cmd_current, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        print("=" * 50)
        print("2. Verificando histórico de migrations:")
        cmd_history = [sys.executable, "-m", "alembic", "history"]
        result = subprocess.run(cmd_history, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        print("=" * 50)
        print("3. Executando upgrade para aplicar a migration:")
        cmd_upgrade = [sys.executable, "-m", "alembic", "upgrade", "head"]
        result = subprocess.run(cmd_upgrade, capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ Migration executada com sucesso!")
            
            # Verificar o status final
            print("=" * 50)
            print("4. Status final das migrations:")
            cmd_final = [sys.executable, "-m", "alembic", "current"]
            result = subprocess.run(cmd_final, capture_output=True, text=True)
            print(result.stdout)
            
        else:
            print(f"❌ Erro na execução (código: {result.returncode})")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()