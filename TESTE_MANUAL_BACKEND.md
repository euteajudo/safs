# 🧪 Teste Manual do Backend FastAPI

## ✅ Verificar se o Servidor Está Funcionando

### **1. Health Check - Teste no Navegador**
Abra seu navegador e acesse:
```
http://localhost:8000/api/v1/health
```

**Resposta Esperada:**
```json
{
  "status": "ok",
  "message": "API do Catálogo de Processos está no ar!"
}
```

### **2. Documentação Swagger**
Acesse no navegador:
```
http://localhost:8000/docs
```

**Você deve ver:**
- Interface do Swagger UI
- Lista de endpoints disponíveis
- Seções organizadas por tags (Login, Usuários, etc.)

### **3. Documentação ReDoc (Alternativa)**
Acesse no navegador:
```
http://localhost:8000/redoc
```

### **4. Schema OpenAPI**
Acesse no navegador:
```
http://localhost:8000/openapi.json
```
**Deve retornar:** JSON com a definição completa da API

## 🔐 Testar Autenticação

### **Via Swagger UI (Recomendado)**
1. Acesse: http://localhost:8000/docs
2. Procure o endpoint `POST /api/v1/token`
3. Clique em "Try it out"
4. Preencha:
   - **username**: `teste2`
   - **password**: `123456`
5. Clique em "Execute"

**Resposta Esperada (se usuário existir):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "teste2",
    "nome": "Nome do Usuário",
    "email": "email@example.com",
    "unidade": "SAFS",
    "is_active": true,
    "is_superuser": false,
    ...
  }
}
```

### **Via curl (Se disponível)**
```bash
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teste2&password=123456"
```

### **Via PowerShell**
```powershell
$body = @{
    username = "teste2"
    password = "123456"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/token" -Method Post -Body $body
```

## 🔧 Script de Teste Automático

Execute o arquivo:
```
C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\test_api.bat
```

Ou no PowerShell:
```powershell
python "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\test_backend_api.py"
```

## ⚠️ Possíveis Problemas

### **1. Servidor não responde:**
- Verifique se o servidor está realmente rodando
- Confirme a porta 8000 no console
- Teste com `http://127.0.0.1:8000` em vez de `localhost`

### **2. Documentação não aparece:**
- Limpe o cache do navegador
- Tente em modo incógnito/privado
- Verifique se não há bloqueadores de conteúdo

### **3. Login falha (401):**
- Usuário `teste2` pode não existir no banco
- Execute a migration: `alembic upgrade head`
- Verifique se há usuários no banco de dados

### **4. Erro de CORS:**
- Verifique se o CORS está configurado no `main.py`
- Confirme se o frontend está na lista de origens permitidas

## 📊 Status dos Testes

Marque conforme testa:

- [ ] ✅ Health Check funcionando
- [ ] ✅ Documentação Swagger acessível  
- [ ] ✅ Schema OpenAPI disponível
- [ ] ✅ Login com credenciais válidas
- [ ] ✅ Rejeição de credenciais inválidas
- [ ] ✅ Endpoints protegidos requerem autenticação

## 🎯 Próximo Passo

Se todos os testes passarem, o backend está funcionando corretamente e você pode:
1. Iniciar o frontend: `npm run dev`
2. Testar o login completo via interface
3. Conectar todos os módulos do sistema