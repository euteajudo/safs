# 🔧 Guia de Resolução - Erro de Conexão Frontend ↔ Backend

## 🚨 Problema Atual
O frontend Next.js está apresentando erro "Failed to fetch" ao tentar se comunicar com o backend FastAPI, mesmo com as correções anteriores implementadas.

## 🔍 Diagnóstico Realizado

### ✅ **Backend Status** - FUNCIONANDO
- ✅ Backend está rodando na porta 8000
- ✅ Health check responde em `http://localhost:8000/api/v1/health`
- ✅ Health check responde em `http://10.28.130.20:8000/api/v1/health`
- ✅ CORS está configurado corretamente

### ❓ **Frontend Status** - PROBLEMAS DE CONECTIVIDADE
- ❌ Frontend não consegue se conectar com o backend
- ❌ Erro "Failed to fetch" persiste
- ❌ Possível problema na configuração de URL da API

## 🛠️ Correções Implementadas

### 1. **Melhorias no arquivo `api.ts`**
- ✅ Forçar uso de `localhost:8000` sempre
- ✅ Logs detalhados para debug
- ✅ Melhor tratamento de erros

### 2. **Ferramentas de Debug Criadas**
- ✅ `debug_frontend_connection.html` - Teste direto no navegador
- ✅ `test_nextjs_connection.js` - Script para console do Next.js
- ✅ Logs detalhados em todas as funções de API

## 🚀 Passos para Resolver

### **Passo 1: Verificar Backend**
```bash
# 1. Confirmar que o backend está rodando
cd backend/backend
python main.py

# 2. Testar manualmente
python -c "import requests; print(requests.get('http://localhost:8000/api/v1/health').json())"
```

### **Passo 2: Reiniciar Frontend com Logs**
```bash
# 1. Parar o Next.js (Ctrl+C)
# 2. Limpar cache
cd dashboard
rm -rf .next
npm run build
npm run dev

# 3. Abrir console do navegador para ver logs detalhados
```

### **Passo 3: Executar Testes de Debug**

#### **Opção A: Teste HTML Direto**
1. Abra `debug_frontend_connection.html` no navegador
2. Execute todos os testes
3. Verifique qual URL funciona

#### **Opção B: Teste no Console do Next.js**
1. Acesse a aplicação Next.js no navegador
2. Abra o console (F12)
3. Cole o conteúdo de `test_nextjs_connection.js`
4. Execute `fullTest()`

### **Passo 4: Verificar Configurações Específicas**

#### **A. Verificar arquivo `.env.local` (se existir)**
```bash
# Verificar se existe configuração de API_URL
cat dashboard/.env.local
```

#### **B. Verificar Next.js Config**
- Arquivo `next.config.ts` deve estar limpo (sem proxy/rewrites)
- Não deve haver middleware interferindo nas requisições de API

#### **C. Verificar Firewall/Antivírus**
- Temporariamente desabilitar firewall
- Verificar se antivírus está bloqueando conexões localhost

### **Passo 5: Soluções Alternativas**

#### **Solução A: Usar Proxy do Next.js**
Adicionar em `next.config.ts`:
```typescript
const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/backend/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};
```

Atualizar `api.ts`:
```typescript
const BASE_URL = '/api/backend';
```

#### **Solução B: Configurar HTTPS no Backend**
```python
# Em main.py, adicionar:
import uvicorn
import ssl

if __name__ == "__main__":
    uvicorn.run(
        "app_catalogo.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        ssl_keyfile="key.pem",  # Se tiver certificado
        ssl_certfile="cert.pem"
    )
```

#### **Solução C: Usar IP específico**
Forçar backend a rodar em IP específico:
```bash
cd backend/backend
python -c "
import uvicorn
from app_catalogo.main import app
uvicorn.run(app, host='10.28.130.20', port=8000)
"
```

## 🔍 Debug em Tempo Real

### **Logs para Monitorar**

#### **No Console do Navegador:**
```javascript
// Verificar se a função de API está sendo chamada
console.log('API URL:', window.location.origin);

// Testar fetch diretamente
fetch('http://localhost:8000/api/v1/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

#### **No Terminal do Backend:**
```bash
# Adicionar logs mais verbosos
cd backend/backend
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
exec(open('main.py').read())
"
```

## 🎯 Identificação da Causa Raiz

### **Possíveis Causas (em ordem de probabilidade):**

1. **🔥 Configuração de URL da API** (mais provável)
   - Frontend tentando usar IP da rede em vez de localhost
   - Configuração inconsistente entre desenvolvimento e produção

2. **🔒 Problema de CORS** (moderado)
   - Headers CORS não configurados corretamente
   - Preflight requests falhando

3. **🚫 Firewall/Segurança** (moderado)
   - Windows Firewall bloqueando conexões
   - Antivírus interferindo

4. **⚙️ Configuração do Next.js** (baixo)
   - Middleware interferindo
   - Configuração de proxy incorreta

5. **🌐 Problema de Rede** (baixo)
   - DNS local
   - Configuração de rede

## 📋 Checklist de Verificação

- [ ] Backend rodando e respondendo em localhost:8000
- [ ] Frontend usando URL correta (localhost:8000)
- [ ] Console do navegador mostrando logs detalhados
- [ ] Testes de debug executados
- [ ] Firewall/antivírus verificados
- [ ] Cache do Next.js limpo
- [ ] Variáveis de ambiente verificadas

## 🆘 Se Nada Funcionar

### **Solução de Emergência: Servidor de Desenvolvimento Unificado**
```bash
# 1. Parar ambos os servidores

# 2. Criar servidor único que serve frontend e backend
cd backend/backend
pip install fastapi-static-files

# 3. Modificar main.py para servir arquivos estáticos do Next.js
# 4. Build do Next.js para pasta static
# 5. Rodar tudo em uma porta só
```

## 📞 Próximos Passos

1. **Execute os testes de debug**
2. **Monitore os logs detalhados**
3. **Identifique qual URL funciona**
4. **Ajuste a configuração conforme necessário**
5. **Teste novamente a criação de itens no catálogo**

---

**🎯 Objetivo:** Estabelecer comunicação estável entre frontend (Next.js) e backend (FastAPI) para resolver o erro "Failed to fetch" definitivamente.
