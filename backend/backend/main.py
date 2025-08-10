"""
Ponto de entrada principal da aplicação FastAPI
"""

import sys
import os

# Adiciona o diretório atual ao PYTHONPATH para resolver importações
if __name__ == "__main__":
    # Garante que o diretório backend está no path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

# Importa e expõe a aplicação FastAPI
from app_catalogo.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
