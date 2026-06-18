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


def insertar_usuario(datos):
    """
    PROPÓSITO: inserta nuevo usuario.

    CODER: Fernanda.

    PARÁMETROS:  
    	:datos: (list): apellido, nombre, clave, id_rol

    RETORNO: 
    	:return: exito (bool).
    
    ERRORES:  (si aplica)
    	:raises: [TipoError] Condición bajo la cual lanza esta excepción.
    """
    
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    query = """
        INSERT INTO Usuario (apellido, nombre, clave, id_rol, activo) 
        VALUES (%s, %s, %s, %s, 1)
    """
    
    try:
        cursor.execute(query, (
            datos['apellido'], 
            datos['nombre'], 
            datos['clave'], 
            datos['id_rol']
        ))
        conexion.commit()
        exito = True
    except Exception as e:
        conexion.rollback()
        print(f"Error al insertar usuario: {e}")
        exito = False
    finally:
        cursor.close()
        conexion.close()
        
    return exito


def obtener_producto_por_id(id):
    """
    PROPÓSITO: Consulta en la base de datos un producto específico mediante su ID unívoco 
               y mapea las columnas relacionales.

    CODER: Fernanda.

    PARÁMETROS:  
        :id: (int) Identificador único del producto en la tabla Producto.

    RETORNO: 
        :producto: (dict o None), Diccionario indexado por nombre de columna si el registro 
                   existe, o None si no se encuentra en el catálogo.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    
    query = "SELECT id_producto, id_categoria, descripcion, marca, precio_compra, precio_venta, stock, activo FROM Producto WHERE id_producto = %s"
    cursor.execute(query, (id,))
    
    producto = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    
    return producto



def listar_proveedores_activos():
    """
    PROPÓSITO: Recupera el catálogo completo de proveedores comerciales vigentes (con alta lógica).
               Utilizado para alimentar dinámicamente Comboboxes de la interfaz.

    CODER: Fernanda.

    PARÁMETROS:  
        Ninguno.

    RETORNO: 
        :proveedores: (list), Lista de diccionarios, donde cada índice representa un proveedor 
                      activo estructurado como {'id_proveedor': int, 'razon_social': str, 'telefono': str}.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    
    query = "SELECT id_proveedor, razon_social, telefono FROM Proveedor WHERE activo = 1"
    cursor.execute(query)
    
    proveedores = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return proveedores