"""
Teste final das rotas de responsáveis técnicos
"""
import requests
import json

API_BASE_URL = "http://localhost:8000/api/v1"

def test_responsavel_tecnico_routes():
    """Testar as rotas de responsáveis técnicos"""
    
    print("=== TESTE DAS ROTAS DE RESPONSÁVEIS TÉCNICOS ===\n")
    
    # 1. Primeiro, testar sem autenticação para ver se a rota existe
    print("1. Testando rota GET sem autenticação...")
    try:
        response = requests.get(f"{API_BASE_URL}/catalogo/1/responsaveis_tecnicos")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
        
        if response.status_code == 401:
            print("   OK: Rota existe (erro 401 = precisa autenticacao)")
        elif response.status_code == 404:
            print("   ERRO: Rota nao encontrada (404)")
        else:
            print(f"   AVISO: Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"   ERRO na requisicao: {e}")
    
    print("\n2. Testando rota POST sem autenticação...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/catalogo/1/responsaveis_tecnicos",
            json=[1, 2]
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
        
        if response.status_code == 401:
            print("   OK: Rota existe (erro 401 = precisa autenticacao)")
        elif response.status_code == 404:
            print("   ERRO: Rota nao encontrada (404)")
        else:
            print(f"   AVISO: Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"   ERRO na requisicao: {e}")
    
    # 3. Testar rota de teste que adicionamos
    print("\n3. Testando rota de teste...")
    try:
        response = requests.get(f"{API_BASE_URL}/catalogo/test-responsaveis")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   OK: Rota de teste funciona")
        elif response.status_code == 401:
            print("   AVISO: Rota de teste precisa autenticacao")
        elif response.status_code == 404:
            print("   ERRO: Rota de teste nao encontrada")
            
    except Exception as e:
        print(f"   ERRO na requisicao: {e}")
    
    # 4. Listar todas as rotas disponíveis do catálogo
    print("\n4. Testando rotas existentes do catálogo...")
    
    test_routes = [
        f"{API_BASE_URL}/catalogo/1/compradores",
        f"{API_BASE_URL}/catalogo/1/controladores", 
        f"{API_BASE_URL}/catalogo/1/responsaveis_tecnicos"
    ]
    
    for route in test_routes:
        try:
            response = requests.get(route)
            route_name = route.split('/')[-1]
            print(f"   {route_name}: {response.status_code}")
        except:
            print(f"   {route_name}: ERRO")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    test_responsavel_tecnico_routes()