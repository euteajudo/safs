#!/usr/bin/env python3
"""Verificar rotas registradas na aplicação"""

import sys
import os

# Adicionar o caminho do backend
sys.path.insert(0, os.path.join('backend', 'backend'))

try:
    from app_catalogo.main import app
    
    print("🔍 Verificando rotas registradas na aplicação FastAPI:")
    print("=" * 60)
    
    for route in app.routes:
        if hasattr(route, 'path'):
            methods = getattr(route, 'methods', ['GET'])
            print(f"  {route.path:<40} {list(methods)}")
    
    print("\n📊 Resumo:")
    total_routes = len([r for r in app.routes if hasattr(r, 'path')])
    print(f"  Total de rotas: {total_routes}")
    
    # Verificar rotas do catálogo especificamente
    catalog_routes = [r for r in app.routes if hasattr(r, 'path') and '/catalogo' in r.path]
    print(f"  Rotas do catálogo: {len(catalog_routes)}")
    
    if catalog_routes:
        print("\n📝 Rotas do catálogo:")
        for route in catalog_routes:
            methods = getattr(route, 'methods', ['GET'])
            print(f"    {route.path:<35} {list(methods)}")
    
    print(f"\n🌐 Documentação disponível em:")
    print(f"  http://localhost:8000/docs")
    print(f"  http://localhost:8000/redoc")
    
except Exception as e:
    print(f"❌ Erro ao importar aplicação: {e}")
    import traceback
    traceback.print_exc()
