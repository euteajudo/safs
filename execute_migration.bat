@echo off
echo Executando migration para remover processo_id e is_responsavel_tecnico...
cd /d "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"

echo.
echo ===== Status atual das migrations =====
python -m alembic current

echo.
echo ===== Historico das migrations =====
python -m alembic history --verbose

echo.
echo ===== Executando upgrade =====
python -m alembic upgrade head

echo.
echo ===== Status final =====
python -m alembic current

echo.
echo Migration concluída!
pause