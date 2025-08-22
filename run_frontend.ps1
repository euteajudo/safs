# Script para executar o frontend do SAFS
Write-Host "Iniciando o frontend do SAFS..." -ForegroundColor Green

# Navegar para o diretório do dashboard
Set-Location -Path "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\dashboard"

# Verificar se node_modules existe
if (-Not (Test-Path "node_modules")) {
    Write-Host "Instalando dependências..." -ForegroundColor Yellow
    npm install
}

# Executar o servidor de desenvolvimento
Write-Host "Iniciando servidor de desenvolvimento na porta 3000..." -ForegroundColor Green
npm run dev