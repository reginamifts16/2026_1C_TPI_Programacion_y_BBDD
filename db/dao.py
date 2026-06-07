"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: dao.py
CAPA: Acceso a Datos / Persistencia (Data Access Object)
DESCRIPCIÓN:
Encapsula el acceso a la base de datos mediante el patrón DAO. Contiene 
las consultas SQL y transacciones puras para independizar la lógica de negocio.
CODER ZERO: Regina
===============================================================================
"""

from db.connection import conectar_bd

def obtener_usuario_por_username(username_ingresado):
    """
    PROPÓSITO: genera el username con nombre y apellido y compara con la BD.

    CODER: Regina.

    PARÁMETROS:  
    	:username: (str) Nombre y apellido     	

    RETORNO: 
    	:return: Identificador (str).
    
    ERRORES:  (si aplica)
    	:raises: [TipoError] Condición bajo la cual lanza esta excepción.
    """


    conn = conectar_bd()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    
    # LOWER y REPLACE remueven mayúsculas y espacios para que el username sea limpio
    query = """
        SELECT u.nombre, u.apellido, u.clave, u.activo, r.rol,
               LOWER(REPLACE(CONCAT(u.nombre, u.apellido), ' ', '')) AS username
        FROM Usuario u
        JOIN Rol r ON u.id_rol = r.id_rol
        HAVING username = LOWER(%s)
    """
    
    cursor.execute(query, (username_ingresado,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado