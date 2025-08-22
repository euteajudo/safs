#!/usr/bin/env python3
"""Popular catálogo com dados de teste"""

import requests
import json

# 1. Login
print("Fazendo login...")
login_response = requests.post(
    'http://127.0.0.1:8000/api/v1/token',
    data={'username': 'teste', 'password': 'teste123'}
)

if login_response.status_code != 200:
    print(f"Erro no login: {login_response.text}")
    exit(1)

token = login_response.json()['access_token']
print("✅ Login OK")

# 2. Criar alguns itens de teste
itens_teste = [
    {
        "unidade": "ULOG",
        "codigo_master": "2589",
        "descritivo_resumido": "LUVA DE PROCEDIMENTO",
        "descritivo_detalhado": "Luva de procedimento não estéril, látex, tamanho M",
        "apresentacao": "Caixa com 100 unidades",
        "classificacao_xyz": "A",
        "catmat": "123456",
        "observacao": "Item de alta rotatividade"
    },
    {
        "unidade": "ULOG",
        "codigo_master": "985647",
        "descritivo_resumido": "Seringa de 0,50ml luerlok",
        "descritivo_detalhado": "Seringa descartável com agulha, capacidade 0,50ml",
        "apresentacao": "Unidade",
        "classificacao_xyz": "B",
        "codigo_aghu_hu": "HU985647"
    },
    {
        "unidade": "ULOG",
        "codigo_master": "87487",
        "descritivo_resumido": "Seringa de 10ml",
        "descritivo_detalhado": "Seringa descartável sem agulha, capacidade 10ml",
        "apresentacao": "Unidade",
        "classificacao_xyz": "A",
        "codigo_ebserh": "EB87487"
    },
    {
        "unidade": "ULOG",
        "codigo_master": "89564",
        "descritivo_resumido": "Algodão hidrófilo",
        "descritivo_detalhado": "Algodão hidrófilo em rolo, 500g",
        "apresentacao": "Rolo 500g",
        "classificacao_xyz": "A"
    },
    {
        "unidade": "ULOG",
        "codigo_master": "6543221",
        "descritivo_resumido": "Gaze estéril",
        "descritivo_detalhado": "Compressa de gaze estéril 7,5x7,5cm, 13 fios",
        "apresentacao": "Pacote com 10 unidades",
        "classificacao_xyz": "A",
        "catmat": "654321"
    }
]

print(f"\nCriando {len(itens_teste)} itens de teste...")
created_count = 0
errors = []

for item in itens_teste:
    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/v1/catalogo',
            json=item,
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code == 201:
            created_item = response.json()
            print(f"  ✅ Criado: {item['codigo_master']} - {item['descritivo_resumido']} (ID: {created_item['id']})")
            created_count += 1
        elif response.status_code == 409:
            print(f"  ⚠️  Item {item['codigo_master']} já existe")
        else:
            errors.append(f"{item['codigo_master']}: {response.text}")
            print(f"  ❌ Erro ao criar {item['codigo_master']}: {response.status_code}")
    except Exception as e:
        errors.append(f"{item['codigo_master']}: {str(e)}")
        print(f"  ❌ Erro ao criar {item['codigo_master']}: {e}")

print(f"\n📊 Resumo:")
print(f"  ✅ {created_count} itens criados com sucesso")
if errors:
    print(f"  ❌ {len(errors)} erros:")
    for error in errors:
        print(f"    - {error}")

# 3. Verificar total de itens
print("\n📦 Verificando catálogo...")
catalog_response = requests.get(
    'http://127.0.0.1:8000/api/v1/catalogo/',
    headers={'Authorization': f'Bearer {token}'}
)

if catalog_response.status_code == 200:
    items = catalog_response.json()
    print(f"  Total de itens no catálogo: {len(items)}")
    if items:
        print("\n  Primeiros 5 itens:")
        for item in items[:5]:
            print(f"    ID: {item['id']}, Código: {item['codigo_master']}, Descrição: {item['descritivo_resumido']}")
else:
    print(f"  Erro ao buscar catálogo: {catalog_response.status_code}")
