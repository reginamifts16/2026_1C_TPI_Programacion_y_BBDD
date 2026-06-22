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

if errorlevel 1 (
    echo.
    echo La aplicacion finalizo con errores.
    pause
) else (
    echo.
    echo La aplicacion finalizo.
)