#!/usr/bin/env python3
"""Simular requisição exata do frontend"""

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
    print(f"✅ Login OK\n")
    
    # 2. Buscar primeiro item para testar
    print("2. Buscando itens...")
    items_response = requests.get(
        'http://127.0.0.1:8000/api/v1/catalogo/',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if items_response.status_code == 200 and items_response.json():
        item = items_response.json()[0]
        print(f"✅ Primeiro item: ID {item['id']}, Código: {item['codigo_master']}\n")
        
        # 3. Simular requisição PATCH do frontend
        print("3. Testando atualização (simulando frontend)...")
        
        # Dados que o frontend enviaria
        update_data = {
            "unidade": item['unidade'],
            "codigo_master": item['codigo_master'],
            "descritivo_resumido": item['descritivo_resumido'],
            "observacao": "Teste via frontend simulado"
        }
        
        print(f"Dados enviados: {json.dumps(update_data, indent=2)}\n")
        
        # Teste direto no backend
        print("4. Teste direto no backend...")
        backend_response = requests.patch(
            f'http://127.0.0.1:8000/api/v1/catalogo/{item["id"]}',
            json=update_data,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )
        
        print(f"Backend - Status: {backend_response.status_code}")
        if backend_response.status_code != 200:
            print(f"Backend - Erro: {backend_response.text}")
        else:
            print("Backend - ✅ OK")
        
        # Teste via proxy Next.js
        print("\n5. Teste via proxy Next.js...")
        try:
            proxy_response = requests.patch(
                f'http://localhost:3000/api/backend/v1/catalogo/{item["id"]}',
                json=update_data,
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
            )
            
            print(f"Proxy - Status: {proxy_response.status_code}")
            if proxy_response.status_code != 200:
                print(f"Proxy - Headers: {dict(proxy_response.headers)}")
                print(f"Proxy - Erro: {proxy_response.text[:500]}")
            else:
                print("Proxy - ✅ OK")
        except Exception as e:
            print(f"Proxy - ❌ Erro de conexão: {e}")
            
        # Teste com dados mínimos
        print("\n6. Teste com dados mínimos...")
        minimal_data = {"observacao": "teste minimo"}
        
        minimal_response = requests.patch(
            f'http://127.0.0.1:8000/api/v1/catalogo/{item["id"]}',
            json=minimal_data,
            headers={'Authorization': f'Bearer {token}'}
        )
        
        print(f"Minimal - Status: {minimal_response.status_code}")
        if minimal_response.status_code != 200:
            print(f"Minimal - Erro: {minimal_response.text}")
        else:
            print("Minimal - ✅ OK")
            
    else:
        print("❌ Nenhum item encontrado no catálogo")
else:
    print(f"❌ Login falhou: {login_response.text}")
