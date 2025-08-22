/**
 * Script para testar conectividade do Next.js com o backend
 * Execute este arquivo no console do navegador quando estiver na aplicação Next.js
 */

console.log('🚀 Iniciando teste de conectividade do Next.js...');

// Função para testar uma URL específica
async function testUrl(url, description) {
  console.log(`\n🔍 Testando: ${description}`);
  console.log(`📍 URL: ${url}`);
  
  try {
    const startTime = Date.now();
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      mode: 'cors'
    });
    
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    console.log(`⏱️  Tempo de resposta: ${duration}ms`);
    console.log(`📊 Status: ${response.status} ${response.statusText}`);
    console.log(`✅ OK: ${response.ok}`);
    
    // Mostrar headers importantes
    const importantHeaders = ['access-control-allow-origin', 'content-type', 'server'];
    console.log('📋 Headers importantes:');
    importantHeaders.forEach(header => {
      const value = response.headers.get(header);
      if (value) {
        console.log(`   ${header}: ${value}`);
      }
    });
    
    if (response.ok) {
      try {
        const data = await response.json();
        console.log('📦 Dados recebidos:', data);
        return { success: true, data, status: response.status, duration };
      } catch (jsonError) {
        console.log('⚠️  Resposta não é JSON válido');
        const text = await response.text();
        console.log('📄 Resposta como texto:', text.substring(0, 200) + '...');
        return { success: true, data: text, status: response.status, duration };
      }
    } else {
      console.log('❌ Resposta não OK');
      try {
        const errorData = await response.json();
        console.log('❌ Dados do erro:', errorData);
      } catch {
        const errorText = await response.text();
        console.log('❌ Texto do erro:', errorText);
      }
      return { success: false, status: response.status, duration };
    }
    
  } catch (error) {
    console.log('💥 Erro de rede/conexão:');
    console.log(`   Nome: ${error.name}`);
    console.log(`   Mensagem: ${error.message}`);
    console.log(`   Stack:`, error.stack);
    
    // Verificar tipo específico do erro
    if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
      console.log('🚨 DIAGNÓSTICO: Erro "Failed to fetch" - possíveis causas:');
      console.log('   1. Backend não está rodando');
      console.log('   2. Problema de CORS');
      console.log('   3. Firewall/antivírus bloqueando');
      console.log('   4. Problema de rede local');
    }
    
    return { success: false, error: error.message };
  }
}

// Função principal de teste
async function runAllTests() {
  console.log('🎯 Informações do ambiente:');
  console.log(`   Origin atual: ${window.location.origin}`);
  console.log(`   Host: ${window.location.hostname}`);
  console.log(`   Port: ${window.location.port}`);
  console.log(`   Protocol: ${window.location.protocol}`);
  console.log(`   User Agent: ${navigator.userAgent}`);
  
  // URLs para testar
  const testUrls = [
    { url: 'http://localhost:8000/api/v1/health', desc: 'Localhost Health Check' },
    { url: 'http://127.0.0.1:8000/api/v1/health', desc: '127.0.0.1 Health Check' },
    { url: 'http://10.28.130.20:8000/api/v1/health', desc: 'Network IP Health Check' }
  ];
  
  const results = [];
  
  for (const test of testUrls) {
    const result = await testUrl(test.url, test.desc);
    results.push({ ...test, result });
    
    // Pequena pausa entre testes
    await new Promise(resolve => setTimeout(resolve, 500));
  }
  
  // Resumo dos resultados
  console.log('\n📊 RESUMO DOS TESTES:');
  console.log('=' .repeat(50));
  
  results.forEach(({ desc, result }) => {
    const status = result.success ? '✅ SUCESSO' : '❌ FALHA';
    const details = result.success 
      ? `(${result.status}, ${result.duration}ms)`
      : `(${result.error || 'Erro desconhecido'})`;
    console.log(`${status} ${desc} ${details}`);
  });
  
  // Recomendações baseadas nos resultados
  const successCount = results.filter(r => r.result.success).length;
  
  console.log('\n💡 RECOMENDAÇÕES:');
  if (successCount === 0) {
    console.log('🚨 Nenhum teste passou - Backend provavelmente não está rodando');
    console.log('   Verifique se o servidor FastAPI está ativo na porta 8000');
  } else if (successCount < results.length) {
    console.log('⚠️  Alguns testes falharam - Problema de configuração de rede');
    console.log('   Considere usar apenas localhost para desenvolvimento');
  } else {
    console.log('🎉 Todos os testes passaram - Conexão OK!');
    console.log('   O problema pode estar na aplicação Next.js ou na autenticação');
  }
  
  return results;
}

// Testar login se os testes básicos passarem
async function testLogin() {
  console.log('\n🔐 Testando processo de login...');
  
  try {
    const formData = new FormData();
    formData.append('username', 'teste2');
    formData.append('password', '123456');
    
    const response = await fetch('http://localhost:8000/api/v1/token', {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      const tokenData = await response.json();
      console.log('✅ Login bem-sucedido!');
      console.log('🎫 Token recebido:', tokenData.access_token ? 'SIM' : 'NÃO');
      console.log('👤 Dados do usuário:', tokenData.user ? 'SIM' : 'NÃO');
      
      // Salvar token temporariamente para outros testes
      if (tokenData.access_token) {
        localStorage.setItem('debug_token', tokenData.access_token);
        console.log('💾 Token salvo no localStorage para testes');
        
        // Testar endpoint autenticado
        await testAuthenticatedEndpoint(tokenData.access_token);
      }
      
      return tokenData;
    } else {
      console.log('❌ Falha no login:', response.status);
      const errorData = await response.json();
      console.log('❌ Erro:', errorData);
      return null;
    }
  } catch (error) {
    console.log('💥 Erro no login:', error.message);
    return null;
  }
}

// Testar endpoint autenticado
async function testAuthenticatedEndpoint(token) {
  console.log('\n🔒 Testando endpoint autenticado (catálogo)...');
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/catalogo?limit=3', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const catalogData = await response.json();
      console.log('✅ Catálogo acessado com sucesso!');
      console.log(`📋 Itens encontrados: ${catalogData.length}`);
      console.log('📦 Primeiros itens:', catalogData.slice(0, 2));
    } else {
      console.log('❌ Falha ao acessar catálogo:', response.status);
      const errorData = await response.json();
      console.log('❌ Erro:', errorData);
    }
  } catch (error) {
    console.log('💥 Erro ao acessar catálogo:', error.message);
  }
}

// Executar todos os testes
async function fullTest() {
  console.clear();
  console.log('🧪 TESTE COMPLETO DE CONECTIVIDADE NEXT.JS → BACKEND');
  console.log('=' .repeat(60));
  
  // Testes básicos de conectividade
  const basicResults = await runAllTests();
  
  // Se pelo menos um teste básico passou, testar login
  const hasConnection = basicResults.some(r => r.result.success);
  if (hasConnection) {
    await testLogin();
  } else {
    console.log('\n⚠️  Pulando teste de login - sem conectividade básica');
  }
  
  console.log('\n🏁 Teste concluído!');
  console.log('💡 Para executar novamente: fullTest()');
}

// Exportar funções para uso manual
window.testNextJSConnection = {
  fullTest,
  runAllTests,
  testLogin,
  testUrl
};

console.log('✅ Funções de teste carregadas!');
console.log('🚀 Execute fullTest() para iniciar os testes completos');
console.log('📋 Ou use testNextJSConnection.testUrl(url, description) para testes específicos');

// Executar teste inicial automaticamente
fullTest();
