@echo off
cd /d "%~dp0"

if not exist env (
    echo.
    echo El entorno virtual no existe.
    echo Ejecute primero setup.bat
    pause
    exit /b
)

call env\Scripts\activate.bat

python main.py

