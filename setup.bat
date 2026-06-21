@echo off
title Configuracion automatica del proyecto
color 0A
cd /d "%~dp0"

echo ============================================
echo     CONFIGURACION AUTOMATICA DEL PROYECTO
echo ============================================
echo.
echo Este asistente realizara las siguientes tareas:
echo.
echo   1. Verificar que Python este instalado.
echo   2. Crear el entorno virtual "env" (si no existe).
echo   3. Instalar las dependencias del proyecto.
echo   4. Permitir ejecutar la demostracion.
echo.
pause

::================================================
:: Verificar Python
::================================================

python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo ============================================
    echo ERROR
    echo ============================================
    echo.
    echo Python no esta instalado o no esta agregado
    echo al PATH del sistema.
    echo.
    echo Descarguelo desde:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b
)

echo.
echo Python encontrado:
python --version
echo.

::================================================
:: Crear entorno virtual
::================================================

if not exist env (
    echo Creando entorno virtual...
    python -m venv env

    if errorlevel 1 (
        echo.
        echo ============================================
        echo ERROR
        echo ============================================
        echo.
        echo No fue posible crear el entorno virtual.
        echo.
        pause
        exit /b
    )
) else (
    echo El entorno virtual ya existe.
)

echo.

::================================================
:: Verificar entorno virtual
::================================================

if not exist env\Scripts\activate.bat (
    echo.
    echo ============================================
    echo ERROR
    echo ============================================
    echo.
    echo No se encontro el archivo de activacion
    echo del entorno virtual.
    echo.
    pause
    exit /b
)

call env\Scripts\activate.bat

::================================================
:: Actualizar pip
::================================================

echo Actualizando pip...
python -m pip install --upgrade pip >nul 2>&1

::================================================
:: Verificar requirements.txt
::================================================

if not exist requirements.txt (
    echo.
    echo ============================================
    echo ERROR
    echo ============================================
    echo.
    echo No se encontro el archivo:
    echo requirements.txt
    echo.
    pause
    exit /b
)

::================================================
:: Instalar dependencias
::================================================

echo.
echo Instalando dependencias...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ============================================
    echo ERROR
    echo ============================================
    echo.
    echo Ocurrio un error durante la instalacion
    echo de las dependencias.
    echo.
    pause
    exit /b
)

echo.
echo ============================================
echo Configuracion completada correctamente.
echo ============================================
echo.

::================================================
:: Ejecutar demostracion
::================================================

choice /M "Desea ejecutar ahora la demostracion"

if errorlevel 2 goto FIN

if exist ejecutar.bat (
    echo.
    echo Iniciando la demostracion...
    echo.
    call ejecutar.bat
    goto FIN
)

echo.
echo ============================================
echo ERROR
echo ============================================
echo.
echo No se encontro el archivo ejecutar.bat
echo.
pause
goto FIN

:FIN

echo.
echo ============================================
echo FIN DEL INSTALADOR
echo ============================================
echo.
echo Si desea ejecutar la demostracion mas tarde:
echo.
echo    1. Ejecute el archivo ejecutar.bat
echo.
echo Gracias por utilizar el instalador.
echo.
pause

exit /b