@echo off
echo ========================================
echo    LIMPEZA COMPLETA DO CACHE NEXT.JS
echo ========================================
echo.

cd dashboard

echo 🧹 Parando servidor Next.js se estiver rodando...
taskkill /F /IM node.exe 2>nul
timeout /t 2 >nul

echo 🗑️  Removendo cache do Next.js...
if exist .next rmdir /s /q .next
if exist node_modules\.cache rmdir /s /q node_modules\.cache

echo 📦 Limpando cache do npm...
npm cache clean --force

echo 🔄 Reinstalando dependências...
npm install

echo 🏗️  Fazendo build limpo...
npm run build

echo ✅ Cache limpo! Agora execute:
echo    npm run dev
echo.
echo ========================================
pause
