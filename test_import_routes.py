#!/usr/bin/env python3
"""Testar importação das rotas para identificar erros"""

import sys
import os

# Adicionar caminho do backend
sys.path.insert(0, os.path.join('backend', 'backend'))

try:
    print("1. Testando importação do módulo base...")
    from app_catalogo.models.base import Base
    print("   ✅ Base importado com sucesso")
    
    print("2. Testando importação dos modelos...")
    from app_catalogo.models.user import User
    from app_catalogo.models.catalogo import ItensCatalogo
    print("   ✅ Modelos importados com sucesso")
    
    print("3. Testando importação dos schemas...")
    from app_catalogo.schemas import catalogo as catalogo_schemas
    print("   ✅ Schemas importados com sucesso")
    
    print("4. Testando importação do security...")
    from app_catalogo.utils import security
    print("   ✅ Security importado com sucesso")
    
    print("5. Testando importação do router do catálogo...")
    from app_catalogo.routers import catalogo
    print("   ✅ Router do catálogo importado com sucesso")
    print(f"   📊 Número de rotas no router: {len(catalogo.router.routes)}")
    
    print("6. Listando rotas do router...")
    for i, route in enumerate(catalogo.router.routes):
        if hasattr(route, 'path'):
            methods = getattr(route, 'methods', ['GET'])
            print(f"   {i+1:2d}. {route.path:<40} {list(methods)}")
    
    print("7. Testando importação da aplicação principal...")
    from app_catalogo.main import app
    print("   ✅ Aplicação principal importada com sucesso")
    
    print("\n🎉 TODAS AS IMPORTAÇÕES FUNCIONARAM!")
    
except Exception as e:
    print(f"\n❌ ERRO NA IMPORTAÇÃO: {e}")
    import traceback
    traceback.print_exc()
