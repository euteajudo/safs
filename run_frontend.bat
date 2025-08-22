@echo off
echo ===================================
echo Iniciando Frontend do SAFS
echo ===================================

cd /d "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\dashboard"

echo.
echo Verificando dependencias...
if not exist node_modules (
    echo Instalando dependencias...
    call npm install
)

echo.
echo Iniciando servidor de desenvolvimento...
echo Acesse: http://localhost:3000
echo.
echo Pressione Ctrl+C para parar o servidor
echo ===================================
call npm run dev