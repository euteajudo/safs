#!/usr/bin/env python3
"""
Script para testar o endpoint HTTP diretamente
"""

import requests
import json

def test_health_endpoint():
    """Testa o endpoint de health check"""
    print("🔍 Testando endpoint de health...")
    try:
        response = requests.get("http://127.0.0.1:8001/api/v1/health", timeout=5)
        print(f"✅ Health check OK! Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
        return False

def test_token_endpoint():
    """Testa o endpoint de token com credenciais do usuário de teste"""
    print("\n🔍 Testando endpoint de token...")
    try:
        # Dados para o login
        data = {
            'username': 'teste2',
            'password': '123456',
            'grant_type': 'password'
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        print(f"📤 Enviando dados: {data}")
        response = requests.post(
            "http://127.0.0.1:8001/api/v1/token", 
            data=data,
            headers=headers,
            timeout=10
        )
        
        print(f"📥 Status recebido: {response.status_code}")
        print(f"📥 Headers da resposta: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login OK! Token recebido.")
            print(f"  Access token: {result.get('access_token', 'N/A')[:50]}...")
            print(f"  Token type: {result.get('token_type', 'N/A')}")
            return True
        else:
            print(f"❌ Login falhou! Status: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"  Erro: {error_detail}")
            except:
                print(f"  Resposta texto: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição de token: {e}")
        return False

def test_cors_headers():
    """Testa se os headers CORS estão configurados"""
    print("\n🔍 Testando headers CORS...")
    try:
        # Faz uma requisição OPTIONS para verificar CORS
        response = requests.options(
            "http://127.0.0.1:8001/api/v1/token",
            headers={'Origin': 'http://localhost:3000'},
            timeout=5
        )
        
        print(f"📥 Status OPTIONS: {response.status_code}")
        print(f"📥 Headers CORS:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower() or 'cors' in header.lower():
                print(f"  {header}: {value}")
                
        return True
    except Exception as e:
        print(f"❌ Erro ao testar CORS: {e}")
        return False

def main():
    print("🚀 Iniciando testes HTTP...\n")
    
    # Teste 1: Health check
    health_ok = test_health_endpoint()
    if not health_ok:
        print("❌ Backend não está respondendo. Verifique se está rodando na porta 8001.")
        return
    
    # Teste 2: CORS headers
    test_cors_headers()
    
    # Teste 3: Token endpoint
    token_ok = test_token_endpoint()
    
    if token_ok:
        print("\n✅ Todos os testes passaram! O backend está funcionando corretamente.")
    else:
        print("\n❌ Falha no teste de token. Verifique as credenciais ou o banco de dados.")

if __name__ == "__main__":
    main()