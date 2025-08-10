import requests

# Teste simples de conectividade
try:
    print("Testando http://127.0.0.1:8001/api/v1/health")
    response = requests.get("http://127.0.0.1:8001/api/v1/health", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.text}")
    
    print("\nTestando login:")
    data = {
        'username': 'teste2',
        'password': '123456'
    }
    
    response = requests.post(
        "http://127.0.0.1:8001/api/v1/token",
        data=data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        timeout=10
    )
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.text}")
    
except Exception as e:
    print(f"ERRO: {e}")