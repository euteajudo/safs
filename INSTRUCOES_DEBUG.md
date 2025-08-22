# INSTRUÇÕES PARA DEBUG DO ERRO 500

## Como identificar o problema:

### 1. Abra o Console do Navegador (F12)

### 2. Tente editar um item no catálogo

### 3. Observe no console:
- Procure pela mensagem: `"📤 Dados sendo enviados:"`
- Veja exatamente quais campos estão sendo enviados

### 4. Verifique se há algum campo problemático:
- Campos com valor `undefined`
- Campos com valor vazio `""`
- Campos com tipos incorretos

## Teste Rápido:

1. **Recarregue a página** (Ctrl+F5)
2. **Abra o console** (F12)
3. **Clique para editar** um dos itens (ID 43-46)
4. **NÃO mude nada**, apenas clique em "Salvando..."
5. **Copie o erro completo** do console

## O que já foi corrigido:

1. ✅ Rotas da API corrigidas (`/v1/catalogo` em vez de `/api/v1/catalogo`)
2. ✅ Proxy configurado para IPv4 (127.0.0.1)
3. ✅ Função `testBackendConnection()` removida (causava erro)
4. ✅ Backend testado e funcionando
5. ✅ Banco populado com dados de teste

## Possíveis causas do erro 500:

1. **Campo com tipo incorreto** sendo enviado
2. **Campo obrigatório faltando**
3. **ID incorreto** (tentando editar item que não existe)
4. **Problema de serialização** JSON

## Como testar manualmente no console:

```javascript
// No console do navegador, execute:
const token = localStorage.getItem('token');
fetch('http://localhost:3000/api/backend/v1/catalogo/43', {
  method: 'PATCH',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    observacao: "Teste manual do console"
  })
}).then(r => r.json()).then(console.log).catch(console.error);
```

Se este teste funcionar, o problema está nos dados que o formulário está enviando.
