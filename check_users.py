#!/usr/bin/env python3
"""Verificar usuários disponíveis"""

import requests

# Login
login_response = requests.post(
    'http://127.0.0.1:8000/api/v1/token',
    data={'username': 'teste', 'password': 'teste123'}
)

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    
    # Buscar usuários
    users_response = requests.get(
        'http://127.0.0.1:8000/api/v1/users',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if users_response.status_code == 200:
        users = users_response.json()
        print(f"Total de usuários: {len(users)}")
        print("\nUsuários disponíveis:")
        for user in users:
            print(f"  ID: {user['id']}, Nome: {user['nome']}, Username: {user['username']}")
    else:
        print(f"Erro ao buscar usuários: {users_response.status_code}")
else:
    print(f"Erro no login: {login_response.status_code}")
