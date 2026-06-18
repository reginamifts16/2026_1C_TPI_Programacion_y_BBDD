@echo off
title Instalador del Proyecto
color 0A
cd /d "%~dp0"

echo ============================================
echo        INSTALADOR DEL PROYECTO
echo ============================================
echo.
echo Este asistente realizara los siguientes pasos:
echo.
echo 1. Verificar que Python este instalado.
echo 2. Crear el entorno virtual "env".
echo 3. Instalar las dependencias.
echo.
pause

::------------------------------------------------
:: Verificar Python
::------------------------------------------------

python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR:
    echo Python no esta instalado o no esta agregado al PATH.
    echo.
    echo Descargalo desde:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b
)

echo.
python --version
echo.
choice /M "Desea crear el entorno virtual"

if errorlevel 2 goto Dependencias

if not exist env (
    python -m venv env

    if errorlevel 1 (
        echo.
        echo No fue posible crear el entorno virtual.
        pause
        exit /b
    )
)

::------------------------------------------------
:: Activar entorno
::------------------------------------------------

:Dependencias

call env\Scripts\activate.bat

echo.
choice /M "¿Desea instalar las dependencias?"

if errorlevel 2 goto Fin

pip install -r requirements.txt

echo.
echo.
echo Instalacion finalizada correctamente.
echo Iniciando la aplicacion...
echo.

call ejecutar.bat

:Fin
