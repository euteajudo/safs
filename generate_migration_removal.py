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
        # Gerar migration com as mudanças nos modelos
        cmd = [
            sys.executable, "-m", "alembic", "revision", 
            "--autogenerate", 
            "-m", "remover_campo_processo_id_e_is_responsavel_tecnico"
        ]
        
        print(f"Executando comando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ Migration gerada com sucesso!")
        else:
            print(f"❌ Erro na execução (código: {result.returncode})")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()