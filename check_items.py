#!/usr/bin/env python3
"""Verificar itens existentes"""

import requests

# Login
login_response = requests.post(
    'http://127.0.0.1:8000/api/v1/token',
    data={'username': 'teste', 'password': 'teste123'}
)

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    
    # Buscar itens
    items_response = requests.get(
        'http://127.0.0.1:8000/api/v1/catalogo/',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if items_response.status_code == 200:
        items = items_response.json()
        print(f"Total de itens: {len(items)}")
        print("\nPrimeiros 10 itens:")
        for item in items[:10]:
            print(f"  ID: {item['id']}, Código: {item['codigo_master']}, Descrição: {item['descritivo_resumido'][:50]}")
    else:
        print(f"Erro ao buscar itens: {items_response.status_code}")
else:
    print(f"Erro no login: {login_response.status_code}")
