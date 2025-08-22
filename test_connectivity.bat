@echo off
echo ========================================
echo    TESTE DE CONECTIVIDADE API SAFS
echo ========================================
echo.

REM Ativar o ambiente virtual se existir
if exist "backend\backend\venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual do backend...
    call backend\backend\venv\Scripts\activate.bat
    echo.
)

REM Executar o script de teste
echo Executando testes de conectividade...
python test_connectivity.py

echo.
echo ========================================
echo Pressione qualquer tecla para continuar...
pause >nul
