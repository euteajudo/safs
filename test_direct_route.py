"""Test direct route access"""
import requests

# Get token
login_response = requests.post(
    "http://localhost:8000/api/v1/token",
    data={"username": "teste2", "password": "123456"}
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test responsaveis_tecnicos route
    response = requests.get(
        "http://localhost:8000/api/v1/catalogo/1/responsaveis_tecnicos",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
else:
    print(f"Login failed: {login_response.status_code}")
    print(login_response.text)