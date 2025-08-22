#!/usr/bin/env python3
"""
Script para iniciar o servidor FastAPI backend
"""

import os
import sys
import subprocess

def main():
    # Caminho para o diretório do backend
    backend_dir = r"C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
    
    # Caminho para o Python
    python_path = r"C:\Python311\python.exe"
    
    # Arquivo principal
    main_file = "main.py"
    
    print("🚀 Iniciando servidor FastAPI...")
    print(f"📂 Diretório: {backend_dir}")
    print(f"🐍 Python: {python_path}")
    print(f"📄 Arquivo: {main_file}")
    print("-" * 50)
    
    try:
        # Muda para o diretório do backend
        os.chdir(backend_dir)
        
        # Executa o servidor
        subprocess.run([python_path, main_file], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar o servidor: {e}")
        return 1
    except FileNotFoundError as e:
        print(f"❌ Arquivo não encontrado: {e}")
        return 1
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())