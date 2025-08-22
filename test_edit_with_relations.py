#!/usr/bin/env python3
"""Testar edição com relacionamentos"""

import requests
import json

# 1. Login
print("Fazendo login...")
login_response = requests.post(
    'http://127.0.0.1:8000/api/v1/token',
    data={'username': 'teste', 'password': 'teste123'}
)

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print("✅ Login OK\n")
    
    # 2. Pegar primeiro item
    items_response = requests.get(
        'http://127.0.0.1:8000/api/v1/catalogo/',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if items_response.status_code == 200 and items_response.json():
        item = items_response.json()[0]
        print(f"Item para editar: ID {item['id']}, Código: {item['codigo_master']}\n")
        
        # 3. Testar diferentes combinações de dados
        test_cases = [
            {
                "name": "Apenas observação",
                "data": {
                    "observacao": "Teste simples"
                }
            },
            {
                "name": "Com campos obrigatórios",
                "data": {
                    "unidade": item['unidade'],
                    "codigo_master": item['codigo_master'],
                    "descritivo_resumido": item['descritivo_resumido'],
                    "observacao": "Teste com campos obrigatórios"
                }
            },
            {
                "name": "Com comprador (ID válido)",
                "data": {
                    "unidade": item['unidade'],
                    "codigo_master": item['codigo_master'],
                    "descritivo_resumido": item['descritivo_resumido'],
                    "comprador_id": 2,  # Diego Sousa
                    "observacao": "Teste com comprador"
                }
            },
            {
                "name": "Com controlador (ID válido)",
                "data": {
                    "unidade": item['unidade'],
                    "codigo_master": item['codigo_master'],
                    "descritivo_resumido": item['descritivo_resumido'],
                    "controlador_id": 1,  # Abimael
                    "observacao": "Teste com controlador"
                }
            },
            {
                "name": "Com responsável técnico (campo singular)",
                "data": {
                    "unidade": item['unidade'],
                    "codigo_master": item['codigo_master'],
                    "descritivo_resumido": item['descritivo_resumido'],
                    "responsavel_tecnico_id": 12,  # Joelson
                    "observacao": "Teste com responsável técnico"
                }
            }
        ]
        
        for test in test_cases:
            print(f"Teste: {test['name']}")
            print(f"Dados: {json.dumps(test['data'], indent=2)}")
            
            # Teste direto no backend
            response = requests.patch(
                f'http://127.0.0.1:8000/api/v1/catalogo/{item["id"]}',
                json=test['data'],
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if response.status_code == 200:
                print(f"✅ Backend OK\n")
            else:
                print(f"❌ Backend erro {response.status_code}: {response.text}\n")
            
            # Teste via proxy
            proxy_response = requests.patch(
                f'http://localhost:3000/api/backend/v1/catalogo/{item["id"]}',
                json=test['data'],
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if proxy_response.status_code == 200:
                print(f"✅ Proxy OK\n")
            else:
                print(f"❌ Proxy erro {proxy_response.status_code}\n")
            
            print("-" * 50 + "\n")
else:
    print(f"❌ Login falhou")
