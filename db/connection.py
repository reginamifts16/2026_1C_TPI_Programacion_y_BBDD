"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: connection.py
CAPA: Acceso a Datos 
DESCRIPCIÓN:
Módulo centralizado de conexión y gestión de la base de datos relacional.
Abstrae la configuración del motor de base de datos y provee el punto de 
acceso unificado para el ciclo de vida de las conexiones en la aplicación.
CODER: Regina
===============================================================================
"""
# correr en consola "python -m pip install mysql-connector-python"
import os
import mysql.connector
from mysql.connector import Error 

def conectar_bd():
    """
    PROPÓSITO: Establece y gestiona la conexión inicial con el motor de base de datos local.
    CODER: Regina
    PARÁMETROS: 
        Ninguno. Usa constantes locales para los parámetros de XAMPP (Puerto 3306).
    RETORNO:     
        :return: Objeto mysql.connector.connection si el enlace es exitoso, o None si falla.
    ERRORES: Captura excepciones de tipo mysql.connector.Error para evitar caídas del sistema.
    """
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="tecno_store_db",
            port=3306
        )
        
        if conexion.is_connected():
            return conexion

    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Cómo usar en las funciones:
# conn = conectar_bd()
# if conn:
#     print("Conexión establecida con éxito.")
#     conn.close()
