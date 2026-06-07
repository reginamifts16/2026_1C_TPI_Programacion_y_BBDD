"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: connection.py
CAPA: Base de Datos
DESCRIPCIÓN:
Módulo centralizado de conexión y gestión de la base de datos relacional.
Abstrae la configuración del motor de base de datos y provee el punto de 
acceso unificado para el ciclo de vida de las conexiones en la aplicación.
CODER: Regina
===============================================================================
"""

# Antes que nada, en consola/terminal:
# pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error

def conectar_bd():
    """
    Establece la conexión con la base de datos tecno_store_db en XAMPP.
    Retorna el objeto de conexión si es exitosa, o None si falla.
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