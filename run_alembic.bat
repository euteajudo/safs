@echo off
cd backend\backend
call venv\Scripts\activate.bat
echo === Checking current Alembic status ===
alembic current
echo.
echo === Showing migration history ===
alembic history
echo.
echo === Applying migrations ===
alembic upgrade head
echo.
echo === Verifying final migration status ===
alembic current
call venv\Scripts\deactivate.bat
pause