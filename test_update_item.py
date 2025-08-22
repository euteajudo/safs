#!/usr/bin/env python3
"""Teste de atualização de item"""

import requests
import json

# 1. Login
print("1. Fazendo login...")
login_response = requests.post(
    'http://127.0.0.1:8000/api/v1/token',
    data={'username': 'teste', 'password': 'teste123'}
)

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print(f"✅ Login OK")
    
    # 2. Tentar atualizar item 3697
    print("\n2. Tentando atualizar item 3697...")
    
    update_data = {
        'observacao': 'Teste de atualização via API'
    }
    
    update_response = requests.patch(
        'http://127.0.0.1:8000/api/v1/catalogo/3697',
        json=update_data,
        headers={'Authorization': f'Bearer {token}'}
    )
    
    print(f"Status: {update_response.status_code}")
    
    if update_response.status_code == 200:
        print("✅ Atualização OK")
        print(f"Resposta: {json.dumps(update_response.json(), indent=2)[:500]}")
    else:
        print(f"❌ Erro na atualização")
        print(f"Resposta: {update_response.text}")
        
    # 3. Testar via proxy
    print("\n3. Testando atualização via proxy Next.js...")
    proxy_response = requests.patch(
        'http://localhost:3000/api/backend/v1/catalogo/3697',
        json=update_data,
        headers={'Authorization': f'Bearer {token}'}
    )
    
    print(f"Status via proxy: {proxy_response.status_code}")
    if proxy_response.status_code == 200:
        print("✅ Proxy OK")
    else:
        print(f"❌ Erro no proxy: {proxy_response.text}")
else:
    print(f"❌ Login falhou: {login_response.text}")
