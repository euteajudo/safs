#!/usr/bin/env python3
"""Teste de autenticação e catálogo"""

import requests

# 1. Login
print("1. Fazendo login...")
login_response = requests.post(
    'http://127.0.0.1:8000/api/v1/token',
    data={'username': 'teste', 'password': 'teste123'}
)

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print(f"✅ Login OK, token obtido")
    
    # 2. Buscar catálogo
    print("\n2. Buscando catálogo...")
    catalog_response = requests.get(
        'http://127.0.0.1:8000/api/v1/catalogo/',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    print(f"Status: {catalog_response.status_code}")
    if catalog_response.status_code == 200:
        items = catalog_response.json()
        print(f"✅ Catálogo OK: {len(items)} itens encontrados")
    else:
        print(f"❌ Erro: {catalog_response.text}")
        
    # 3. Testar via proxy
    print("\n3. Testando via proxy Next.js...")
    proxy_response = requests.get(
        'http://localhost:3000/api/backend/v1/catalogo/',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    print(f"Status via proxy: {proxy_response.status_code}")
    if proxy_response.status_code == 200:
        items = proxy_response.json()
        print(f"✅ Proxy OK: {len(items)} itens encontrados")
    else:
        print(f"❌ Erro no proxy: {proxy_response.text}")
else:
    print(f"❌ Login falhou: {login_response.text}")
