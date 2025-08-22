# 🚀 Como Executar o Backend FastAPI

## Opção 1: Arquivo Batch (Recomendado)
1. Execute o arquivo: `C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\start_backend.bat`
2. O script irá:
   - Navegar para o diretório correto
   - Verificar se o arquivo main.py existe
   - Iniciar o servidor FastAPI

## Opção 2: Terminal Manual
1. Abra o **Prompt de Comando** ou **PowerShell**
2. Execute os seguintes comandos:

```cmd
cd "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
python main.py
```

## Opção 3: PowerShell
```powershell
cd "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
python main.py
```

## ✅ Verificar se o Servidor Está Funcionando

Após executar, você deverá ver uma saída similar a:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX]
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🌐 URLs Importantes

- **API Base**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## 🔐 Testar Autenticação

1. Acesse: http://localhost:8000/docs
2. Vá para o endpoint `/api/v1/token`
3. Clique em "Try it out"
4. Use as credenciais:
   - **username**: `teste2`
   - **password**: `123456`
5. Execute e você deverá receber um token de acesso

## 🛑 Para Parar o Servidor

- Pressione `Ctrl + C` no terminal onde o servidor está rodando

## ⚠️ Problemas Comuns

### Porta já em uso:
Se aparecer erro de porta em uso, você pode:
1. Parar outros serviços na porta 8000
2. Ou modificar a porta no arquivo `main.py` (linha com `port=8000`)

### Dependências em falta:
Se aparecer erro de imports, execute:
```cmd
cd "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
pip install -r requirements.txt
```

### Banco de dados:
Se aparecer erro de banco, execute primeiro a migration:
```cmd
cd "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
python -m alembic upgrade head
```