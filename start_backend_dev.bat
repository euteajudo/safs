@echo off
echo ========================================
echo   SERVIDOR FASTAPI - MODO DESENVOLVIMENTO
echo           (Hot Reload Ativado)
echo ========================================
echo.

cd /d "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"

echo Diretorio atual: %CD%
echo.

echo 🔥 Iniciando servidor com Hot Reload...
echo Servidor estara disponivel em: http://localhost:8000
echo Documentacao da API em: http://localhost:8000/docs
echo.
echo ✨ MODO DESENVOLVIMENTO:
echo - Reinicializacao automatica detectando mudancas
echo - Para parar: Ctrl + C
echo.

uvicorn app_catalogo.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo Servidor encerrado.
pause