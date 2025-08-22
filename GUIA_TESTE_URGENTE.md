# 🚨 GUIA DE TESTE URGENTE - Campo Responsável Técnico

## 🎯 Problema Persistente

O erro continua mesmo após as correções implementadas. Vamos fazer um diagnóstico completo.

## 🧪 Testes para Executar (EM ORDEM)

### **1. Teste de Cache do Next.js**
```bash
# Execute este comando para limpar completamente o cache:
clear_nextjs_cache.bat

# OU manualmente:
cd dashboard
taskkill /F /IM node.exe
rm -rf .next
rm -rf node_modules/.cache
npm cache clean --force
npm install
npm run build
npm run dev
```

### **2. Teste HTML Direto (SEM Next.js)**
1. Abra o arquivo `test_minimal_request.html` no navegador
2. Execute os testes na ordem:
   - ✅ **Login** → Deve funcionar
   - ✅ **Buscar Usuários** → Deve funcionar  
   - ✅ **Criar SEM Responsável** → Deve funcionar
   - ❌ **Criar COM Responsável** → Aqui deve aparecer o erro

### **3. Verificar Backend**
```bash
# Certificar que o backend está rodando:
cd backend/backend
python main.py

# Testar diretamente:
curl http://localhost:8000/api/v1/health
```

### **4. Teste no Console do Next.js**
Se o teste HTML funcionar mas o Next.js não, o problema é no Next.js.

Cole este código no console do navegador (na aplicação Next.js):
```javascript
// Testar fetch direto
fetch('http://localhost:8000/api/v1/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);

// Testar com dados mínimos
const testData = {
  unidade: "ULOG",
  codigo_master: "TEST_" + Date.now(),
  descritivo_resumido: "Teste direto"
};

fetch('http://localhost:8000/api/v1/catalogo', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('token'),
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(testData)
})
.then(r => r.json())
.then(console.log)
.catch(console.error);
```

## 🔍 Cenários Possíveis

### **Cenário A: Problema no Next.js**
- ✅ Teste HTML funciona
- ❌ Next.js não funciona
- **Solução**: Problema de cache/configuração do Next.js

### **Cenário B: Problema no Backend**
- ❌ Teste HTML não funciona
- ❌ Next.js não funciona
- **Solução**: Problema no backend com o campo responsável técnico

### **Cenário C: Problema de Rede/CORS**
- ❌ Ambos não funcionam
- ❌ Erro "Failed to fetch"
- **Solução**: Problema de conectividade

## 🛠️ Correções Implementadas (Para Referência)

### **Frontend Simplificado:**
```typescript
// NOVA VERSÃO - Mais limpa e segura
const submitData: any = {
  unidade: values.unidade,
  codigo_master: values.codigo_master,
  descritivo_resumido: values.descritivo_resumido
};

// Apenas adicionar responsável técnico se válido
if (values.responsavel_tecnico_id && values.responsavel_tecnico_id.trim()) {
  const responsavelId = parseInt(values.responsavel_tecnico_id);
  if (!isNaN(responsavelId) && responsavelId > 0) {
    submitData.responsavel_tecnico_id = responsavelId;
  }
}
```

### **Backend Robusto:**
```python
# Tratamento seguro de IDs inválidos
if isinstance(responsavel_tecnico_id_singular, (int, str)) and str(responsavel_tecnico_id_singular).strip():
    try:
        id_num = int(responsavel_tecnico_id_singular)
        if id_num > 0:
            responsavel_tecnico_ids = [id_num]
    except (ValueError, TypeError):
        logger.warning(f"ID inválido: {responsavel_tecnico_id_singular}")
```

## 📊 Resultados Esperados

### **✅ Sucesso:**
- Teste HTML: Ambos os casos funcionam
- Next.js: Funciona após limpar cache
- Console: Logs claros sem erros

### **❌ Falha:**
- Teste HTML: Falha no caso COM responsável
- Next.js: Continua falhando
- Console: Erros "Failed to fetch" ou similares

## 🆘 Se Nada Funcionar

### **Solução Extrema 1: Remover Campo Temporariamente**
```typescript
// Comentar completamente o campo responsável técnico
// responsavel_tecnico_id: z.string().optional().or(z.literal("")),
```

### **Solução Extrema 2: Backend Alternativo**
```python
# Ignorar completamente o campo no backend
responsavel_tecnico_id_singular = item_data.pop('responsavel_tecnico_id', None)
# Simplesmente não processar
```

### **Solução Extrema 3: Proxy Next.js**
```typescript
// next.config.ts
const nextConfig = {
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

## 🎯 Próximos Passos

1. **Execute o teste HTML** → Isso vai isolar se o problema é no Next.js ou no backend
2. **Compartilhe os logs** do console (tanto HTML quanto Next.js)
3. **Informe qual cenário** está acontecendo (A, B ou C)

Com essas informações, posso implementar a correção definitiva! 🎯
