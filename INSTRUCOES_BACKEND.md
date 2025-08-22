# 🚀 Instruções para Iniciar o Servidor Backend

## Método 1: Via Prompt de Comando (CMD)

1. **Abra o Prompt de Comando** (tecla Windows + R, digite `cmd` e pressione Enter)

2. **Navegue até o diretório do backend:**
   ```cmd
   cd /d "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
   ```

3. **Execute o servidor:**
   ```cmd
   "C:\Python311\python.exe" main.py
   ```

## Método 2: Via PowerShell

1. **Abra o PowerShell** (tecla Windows + X, selecione "Windows PowerShell")

2. **Execute o comando:**
   ```powershell
   cd "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
   & "C:\Python311\python.exe" main.py
   ```

## Método 3: Via Script Python

1. **Execute o script criado:**
   ```cmd
   cd "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs"
   python start_backend.py
   ```

## Método 4: Via Uvicorn Diretamente

1. **Navegue até o diretório:**
   ```cmd
   cd /d "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
   ```

2. **Execute com uvicorn:**
   ```cmd
   "C:\Python311\python.exe" -m uvicorn app_catalogo.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## ✅ Verificação de Sucesso

Quando o servidor iniciar corretamente, você verá uma mensagem similar a:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxx] using WatchFiles
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🌐 Testando o Servidor

1. **Abra o navegador** e acesse: `http://localhost:8000/docs`
2. **Teste o health check**: `http://localhost:8000/api/v1/health`

## 🔧 Possíveis Problemas

### Erro de Módulo não encontrado
Se aparecer erro de módulo não encontrado, execute:
```cmd
cd /d "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
set PYTHONPATH=%CD%
"C:\Python311\python.exe" main.py
```

### Erro de Porta em Uso
Se a porta 8000 estiver em uso, mude para outra porta:
```cmd
"C:\Python311\python.exe" -m uvicorn app_catalogo.main:app --host 0.0.0.0 --port 8001 --reload
```

### Erro de Dependências
Se houver erro de dependências faltando:
```cmd
"C:\Python311\python.exe" -m pip install fastapi uvicorn sqlalchemy asyncpg python-multipart python-jose bcrypt
```

## 📋 Logs e Debug

Para ver logs detalhados, execute com:
```cmd
"C:\Python311\python.exe" main.py --log-level debug
```

---

**Nota**: Mantenha o terminal/prompt aberto enquanto estiver usando o sistema, pois o servidor estará rodando nele.