#!/usr/bin/env python3
"""
Script para testar a conectividade e funcionamento da API
"""

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_health_check() -> bool:
    """Testa o endpoint de health check"""
    try:
        print("🔍 Testando endpoint de health check...")
        response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK: {data.get('message', 'API funcionando')}")
            return True
        else:
            print(f"❌ Health check falhou: Status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão: Backend não está rodando ou inacessível")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_cors() -> bool:
    """Testa se os headers CORS estão configurados"""
    try:
        print("🔍 Testando configuração CORS...")
        response = requests.options(
            f"{BASE_URL}/api/v1/health",
            headers={
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'GET'
            },
            timeout=5
        )
        
        cors_headers = {k: v for k, v in response.headers.items() 
                       if 'access-control' in k.lower()}
        
        if cors_headers:
            print("✅ Headers CORS configurados:")
            for header, value in cors_headers.items():
                print(f"   {header}: {value}")
            return True
        else:
            print("⚠️  Nenhum header CORS encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar CORS: {e}")
        return False

def test_login() -> str:
    """Testa o login e retorna o token"""
    try:
        print("🔍 Testando login...")
        
        # Dados de login de teste
        login_data = {
            'username': 'teste2',
            'password': '123456'
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/token",
            data=login_data,  # FormData para OAuth2
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('access_token')
            print(f"✅ Login realizado com sucesso!")
            print(f"   Token: {token[:50]}..." if token else "   Sem token retornado")
            return token
        else:
            print(f"❌ Login falhou: Status {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Erro: {error_data.get('detail', 'Erro desconhecido')}")
            except:
                print(f"   Resposta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return None

def test_catalog_endpoint(token: str) -> bool:
    """Testa o endpoint do catálogo"""
    if not token:
        print("❌ Não é possível testar catálogo sem token")
        return False
        
    try:
        print("🔍 Testando endpoint do catálogo...")
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f"{BASE_URL}/api/v1/catalogo?limit=5",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            items = response.json()
            print(f"✅ Catálogo acessível: {len(items)} itens encontrados")
            return True
        else:
            print(f"❌ Erro ao acessar catálogo: Status {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Erro: {error_data.get('detail', 'Erro desconhecido')}")
            except:
                print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar catálogo: {e}")
        return False

def test_create_item(token: str) -> bool:
    """Testa a criação de um item no catálogo"""
    if not token:
        print("❌ Não é possível testar criação sem token")
        return False
        
    try:
        print("🔍 Testando criação de item...")
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Item de teste
        test_item = {
            "unidade": "ULOG",
            "codigo_master": f"TEST{hash('test') % 10000}",  # Código único
            "descritivo_resumido": "Item de teste para verificação da API",
            "descritivo_detalhado": "Este é um item criado automaticamente para testar a conectividade",
            "apresentacao": "Unidade de teste",
            "classificacao_xyz": "Z",
            "responsavel_tecnico": "Sistema de Teste",
            "observacao": "Item criado pelo script de teste - pode ser removido"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/catalogo",
            headers=headers,
            json=test_item,
            timeout=15
        )
        
        if response.status_code == 201:
            item_data = response.json()
            print(f"✅ Item criado com sucesso!")
            print(f"   ID: {item_data.get('id')}")
            print(f"   Código Master: {item_data.get('codigo_master')}")
            return True
        else:
            print(f"❌ Erro ao criar item: Status {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Erro: {error_data.get('detail', 'Erro desconhecido')}")
            except:
                print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar criação: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Iniciando testes de conectividade...\n")
    
    # Testa health check
    health_ok = test_health_check()
    print()
    
    if not health_ok:
        print("❌ Backend não está acessível. Verifique se está rodando em http://localhost:8000")
        sys.exit(1)
    
    # Testa CORS
    cors_ok = test_cors()
    print()
    
    # Testa login
    token = test_login()
    print()
    
    if not token:
        print("❌ Não foi possível fazer login. Verifique as credenciais e o banco de dados.")
        sys.exit(1)
    
    # Testa catálogo
    catalog_ok = test_catalog_endpoint(token)
    print()
    
    # Testa criação
    create_ok = test_create_item(token)
    print()
    
    # Resumo
    print("📊 RESUMO DOS TESTES:")
    print(f"   Health Check: {'✅' if health_ok else '❌'}")
    print(f"   CORS: {'✅' if cors_ok else '⚠️'}")
    print(f"   Login: {'✅' if token else '❌'}")
    print(f"   Catálogo: {'✅' if catalog_ok else '❌'}")
    print(f"   Criação: {'✅' if create_ok else '❌'}")
    
    if all([health_ok, token, catalog_ok, create_ok]):
        print("\n🎉 Todos os testes passaram! A API está funcionando corretamente.")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os problemas acima.")

if __name__ == "__main__":
    main()
