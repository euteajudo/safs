#!/usr/bin/env python3
"""
Script para testar especificamente o campo Responsável Técnico
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def get_auth_token():
    """Obtém token de autenticação"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/token",
            data={
                'username': 'teste2',
                'password': '123456'
            }
        )
        if response.ok:
            return response.json()['access_token']
        else:
            print(f"❌ Erro no login: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        return None

def test_create_item_without_responsavel(token):
    """Testa criação de item SEM responsável técnico"""
    print("\n🧪 Teste 1: Criando item SEM responsável técnico...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    item_data = {
        "unidade": "ULOG",
        "codigo_master": f"TEST_NO_RESP_{hash('test1') % 10000}",
        "descritivo_resumido": "Item de teste sem responsável técnico",
        "descritivo_detalhado": "Este item não tem responsável técnico definido",
        "apresentacao": "Unidade",
        "classificacao_xyz": "Z",
        "observacao": "Teste sem responsável técnico"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/catalogo",
            headers=headers,
            json=item_data
        )
        
        if response.ok:
            result = response.json()
            print(f"✅ Item criado com sucesso! ID: {result['id']}")
            print(f"   Código Master: {result['codigo_master']}")
            return result['id']
        else:
            error_data = response.json()
            print(f"❌ Erro: {response.status_code}")
            print(f"   Detalhes: {error_data}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def test_create_item_with_responsavel(token):
    """Testa criação de item COM responsável técnico"""
    print("\n🧪 Teste 2: Criando item COM responsável técnico...")
    
    # Primeiro, buscar usuários disponíveis
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        users_response = requests.get(f"{BASE_URL}/api/v1/users?limit=10", headers=headers)
        if users_response.ok:
            users = users_response.json()
            if users:
                user_id = users[0]['id']
                print(f"   Usando usuário ID {user_id} ({users[0]['nome']}) como responsável técnico")
            else:
                print("❌ Nenhum usuário encontrado")
                return None
        else:
            print("❌ Erro ao buscar usuários")
            return None
    except Exception as e:
        print(f"❌ Erro ao buscar usuários: {e}")
        return None
    
    item_data = {
        "unidade": "ULOG",
        "codigo_master": f"TEST_WITH_RESP_{hash('test2') % 10000}",
        "descritivo_resumido": "Item de teste com responsável técnico",
        "descritivo_detalhado": "Este item tem responsável técnico definido",
        "apresentacao": "Unidade",
        "classificacao_xyz": "Z",
        "observacao": "Teste com responsável técnico",
        # Campo que estava causando problema
        "responsavel_tecnico_ids": [user_id]  # Usar array
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/catalogo",
            headers=headers,
            json=item_data
        )
        
        if response.ok:
            result = response.json()
            print(f"✅ Item criado com sucesso! ID: {result['id']}")
            print(f"   Código Master: {result['codigo_master']}")
            print(f"   Responsáveis técnicos: {len(result.get('responsaveis_tecnicos', []))}")
            return result['id']
        else:
            error_data = response.json()
            print(f"❌ Erro: {response.status_code}")
            print(f"   Detalhes: {error_data}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def test_create_item_with_invalid_responsavel(token):
    """Testa criação de item com responsável técnico INVÁLIDO"""
    print("\n🧪 Teste 3: Criando item com responsável técnico INVÁLIDO...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    item_data = {
        "unidade": "ULOG",
        "codigo_master": f"TEST_INVALID_{hash('test3') % 10000}",
        "descritivo_resumido": "Item de teste com responsável inválido",
        "responsavel_tecnico_ids": [99999]  # ID que não existe
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/catalogo",
            headers=headers,
            json=item_data
        )
        
        if response.ok:
            result = response.json()
            print(f"✅ Item criado (responsável inválido foi ignorado)")
            print(f"   ID: {result['id']}")
            return result['id']
        else:
            error_data = response.json()
            print(f"❌ Erro esperado: {response.status_code}")
            print(f"   Detalhes: {error_data}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def test_frontend_format(token):
    """Testa o formato que o frontend estava enviando (que causava erro)"""
    print("\n🧪 Teste 4: Testando formato do frontend (responsavel_tecnico_id singular)...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Buscar um usuário válido
    try:
        users_response = requests.get(f"{BASE_URL}/api/v1/users?limit=1", headers=headers)
        if users_response.ok and users_response.json():
            user_id = users_response.json()[0]['id']
        else:
            print("❌ Não foi possível encontrar usuário para teste")
            return None
    except:
        print("❌ Erro ao buscar usuário")
        return None
    
    # Formato que o frontend estava enviando
    item_data = {
        "unidade": "ULOG",
        "codigo_master": f"TEST_FRONTEND_{hash('test4') % 10000}",
        "descritivo_resumido": "Item teste formato frontend",
        # Formato original do frontend (singular)
        "responsavel_tecnico_id": user_id  # Singular, como o frontend enviava
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/catalogo",
            headers=headers,
            json=item_data
        )
        
        if response.ok:
            result = response.json()
            print(f"✅ Item criado com formato frontend!")
            print(f"   ID: {result['id']}")
            print(f"   Responsáveis técnicos: {len(result.get('responsaveis_tecnicos', []))}")
            return result['id']
        else:
            error_data = response.json()
            print(f"❌ Erro: {response.status_code}")
            print(f"   Detalhes: {error_data}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def main():
    print("🧪 TESTE ESPECÍFICO: Campo Responsável Técnico")
    print("=" * 60)
    
    # Obter token
    token = get_auth_token()
    if not token:
        print("❌ Não foi possível obter token de autenticação")
        return
    
    print("✅ Token obtido com sucesso")
    
    # Executar testes
    results = []
    
    # Teste 1: Sem responsável técnico
    result1 = test_create_item_without_responsavel(token)
    results.append(("Sem responsável", result1 is not None))
    
    # Teste 2: Com responsável técnico válido
    result2 = test_create_item_with_responsavel(token)
    results.append(("Com responsável válido", result2 is not None))
    
    # Teste 3: Com responsável técnico inválido
    result3 = test_create_item_with_invalid_responsavel(token)
    results.append(("Com responsável inválido", result3 is not None))
    
    # Teste 4: Formato frontend
    result4 = test_frontend_format(token)
    results.append(("Formato frontend", result4 is not None))
    
    # Resumo
    print("\n📊 RESUMO DOS TESTES:")
    print("=" * 60)
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{status} - {test_name}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\n🎯 Resultado: {total_passed}/{len(results)} testes passaram")
    
    if total_passed == len(results):
        print("🎉 Todos os testes passaram! O campo responsável técnico está funcionando!")
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")

if __name__ == "__main__":
    main()
