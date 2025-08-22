"""
Script para testar as rotas de responsáveis técnicos
"""
import asyncio
import httpx
import json

API_BASE_URL = "http://localhost:8000/api/v1"

# Credenciais de teste (conforme documentação da API)
LOGIN_DATA = {
    "username": "teste2",
    "password": "123456"
}

async def get_token():
    """Obter token de autenticação"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/token",
            data=LOGIN_DATA
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"Erro no login: {response.status_code}")
            print(response.text)
            return None

async def test_responsaveis_tecnicos():
    """Testar rotas de responsáveis técnicos"""
    token = await get_token()
    
    if not token:
        print("Não foi possível obter token de autenticação")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        # 1. Obter lista de itens do catálogo
        print("\n1. Buscando itens do catálogo...")
        response = await client.get(
            f"{API_BASE_URL}/catalogo",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Erro ao buscar itens: {response.status_code}")
            return
        
        itens = response.json()
        if not itens:
            print("Nenhum item encontrado no catálogo")
            return
        
        item_id = itens[0]["id"]
        print(f"Usando item ID: {item_id}")
        
        # 2. Obter lista de usuários para usar como responsáveis técnicos
        print("\n2. Buscando usuários...")
        response = await client.get(
            f"{API_BASE_URL}/users",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Erro ao buscar usuários: {response.status_code}")
            return
        
        usuarios = response.json()
        if len(usuarios) < 2:
            print("Poucos usuários disponíveis para teste")
            return
        
        # Selecionar 2 usuários como responsáveis técnicos
        responsavel_ids = [usuarios[0]["id"], usuarios[1]["id"]]
        print(f"IDs dos responsáveis técnicos selecionados: {responsavel_ids}")
        
        # 3. Associar responsáveis técnicos ao item
        print(f"\n3. Associando responsáveis técnicos ao item {item_id}...")
        response = await client.post(
            f"{API_BASE_URL}/catalogo/{item_id}/responsaveis_tecnicos",
            headers=headers,
            json=responsavel_ids
        )
        
        if response.status_code == 200:
            print("✅ Responsáveis técnicos associados com sucesso!")
            item_atualizado = response.json()
            if "responsaveis_tecnicos" in item_atualizado:
                print(f"Responsáveis técnicos no item: {len(item_atualizado['responsaveis_tecnicos'])}")
                for resp in item_atualizado['responsaveis_tecnicos']:
                    print(f"  - {resp['nome']} ({resp['email']}) - {resp['unidade']}")
        else:
            print(f"❌ Erro ao associar responsáveis: {response.status_code}")
            print(response.text)
        
        # 4. Listar responsáveis técnicos do item
        print(f"\n4. Listando responsáveis técnicos do item {item_id}...")
        response = await client.get(
            f"{API_BASE_URL}/catalogo/{item_id}/responsaveis_tecnicos",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Lista de responsáveis técnicos obtida com sucesso!")
            responsaveis = response.json()
            print(f"Total de responsáveis técnicos: {len(responsaveis)}")
            for resp in responsaveis:
                print(f"  - ID: {resp['id']}, Nome: {resp['nome']}, Email: {resp['email']}, Unidade: {resp['unidade']}")
        else:
            print(f"❌ Erro ao listar responsáveis: {response.status_code}")
            print(response.text)
        
        # 5. Testar remoção de responsáveis (associar lista vazia)
        print(f"\n5. Removendo todos os responsáveis técnicos do item {item_id}...")
        response = await client.post(
            f"{API_BASE_URL}/catalogo/{item_id}/responsaveis_tecnicos",
            headers=headers,
            json=[]
        )
        
        if response.status_code == 200:
            print("✅ Responsáveis técnicos removidos com sucesso!")
        else:
            print(f"❌ Erro ao remover responsáveis: {response.status_code}")
        
        # 6. Verificar se foram removidos
        print(f"\n6. Verificando remoção...")
        response = await client.get(
            f"{API_BASE_URL}/catalogo/{item_id}/responsaveis_tecnicos",
            headers=headers
        )
        
        if response.status_code == 200:
            responsaveis = response.json()
            if len(responsaveis) == 0:
                print("✅ Confirmado: todos os responsáveis técnicos foram removidos")
            else:
                print(f"⚠️ Ainda existem {len(responsaveis)} responsáveis técnicos")
        
        print("\n✅ Teste concluído com sucesso!")

if __name__ == "__main__":
    print("=== TESTE DAS ROTAS DE RESPONSÁVEIS TÉCNICOS ===")
    asyncio.run(test_responsaveis_tecnicos())