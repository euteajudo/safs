@echo off
echo ========================================
echo    INICIANDO SERVIDOR FASTAPI - SAFS
echo ========================================
echo.

cd /d "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"

echo Diretorio atual: %CD%
echo.

echo Verificando arquivo main.py...
if exist main.py (
    echo ✅ Arquivo main.py encontrado
) else (
    echo ❌ Arquivo main.py nao encontrado
    pause
    exit /b 1
)

echo.
echo Iniciando servidor FastAPI...
echo Servidor estara disponivel em: http://localhost:8000
echo Documentacao da API em: http://localhost:8000/docs
echo.

python main.py

echo.
echo Servidor encerrado.
pause