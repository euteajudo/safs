#!/usr/bin/env python3

import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("🔍 TESTANDO API DO BACKEND SAFS")
    print("=" * 50)
    
    # Teste 1: Health Check
    print("\n1️⃣ TESTE: Health Check")
    try:
        response = requests.get(f"{base_url}/api/v1/health", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Resposta: {response.json()}")
        else:
            print(f"   ❌ Erro: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de conexão: {e}")
    
    # Teste 2: Documentação
    print("\n2️⃣ TESTE: Documentação Swagger")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Documentação acessível")
            print(f"   📄 URL: {base_url}/docs")
        else:
            print(f"   ❌ Erro ao acessar docs: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de conexão: {e}")
    
    # Teste 3: OpenAPI JSON
    print("\n3️⃣ TESTE: Schema OpenAPI")
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Schema OpenAPI disponível")
        else:
            print(f"   ❌ Erro: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de conexão: {e}")
    
    # Teste 4: Endpoint de Login
    print("\n4️⃣ TESTE: Endpoint de Login")
    try:
        # Teste com credenciais inválidas primeiro
        data = {
            'username': 'usuario_inexistente',
            'password': 'senha_errada'
        }
        response = requests.post(f"{base_url}/api/v1/token", data=data, timeout=5)
        print(f"   Status (credenciais inválidas): {response.status_code}")
        
        if response.status_code == 401:
            print("   ✅ Validação de credenciais funcionando")
        
        # Agora teste com credenciais válidas (se existirem)
        data = {
            'username': 'teste2',
            'password': '123456'
        }
        response = requests.post(f"{base_url}/api/v1/token", data=data, timeout=5)
        print(f"   Status (teste2/123456): {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Login funcionando!")
            print(f"   🔑 Token gerado: {result.get('access_token', 'N/A')[:20]}...")
            print(f"   👤 Usuário: {result.get('user', {}).get('nome', 'N/A')}")
        elif response.status_code == 401:
            print("   ⚠️  Credenciais teste2/123456 não existem ou estão incorretas")
        else:
            print(f"   ❌ Erro inesperado: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de conexão: {e}")
    
    # Teste 5: Endpoint de usuários (se existir)
    print("\n5️⃣ TESTE: Endpoint de Usuários (sem autenticação)")
    try:
        response = requests.get(f"{base_url}/api/v1/users", timeout=5)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 401:
            print("   ✅ Endpoint protegido - requer autenticação")
        elif response.status_code == 200:
            print("   ⚠️  Endpoint não protegido")
        else:
            print(f"   ℹ️  Outro status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de conexão: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 TESTE CONCLUÍDO")
    print("\n📋 RESUMO:")
    print("   • Health Check: Verifica se API está respondendo")
    print("   • Documentação: Swagger UI deve estar em /docs")
    print("   • Login: Testa autenticação JWT")
    print("   • Proteção: Verifica se rotas estão protegidas")
    
    print(f"\n🌐 URLs Importantes:")
    print(f"   • API: {base_url}")
    print(f"   • Docs: {base_url}/docs")
    print(f"   • Health: {base_url}/api/v1/health")
    print(f"   • Login: {base_url}/api/v1/token")

if __name__ == "__main__":
    test_api()