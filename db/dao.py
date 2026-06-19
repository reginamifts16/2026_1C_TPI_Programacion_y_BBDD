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
    
    # LOWER y REPLACE dejan el username limpio
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
            datos[0], 
            datos[1], 
            datos[2], 
            datos[3]
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


def buscar_productos_por_nombre(termino):
    """
    PROPÓSITO: Busca productos activos en el catálogo cuyo nombre o marca coincidan 
               parcialmente con el término de búsqueda ingresado.

    CODER: Regina.

    PARÁMETROS:  
        :termino: (str) Palabra o fragmento a buscar.

    RETORNO: 
        :resultados: (list) Lista de diccionarios con los productos encontrados.
    """
    conexion = conectar_bd()
    if not conexion:
        return []
        
    cursor = conexion.cursor(dictionary=True)
    # Usamos LIKE con comodines % para buscar coincidencias parciales
    query = """
        SELECT id_producto, descripcion, marca, precio_venta, stock 
        FROM Producto 
        WHERE activo = 1 AND (descripcion LIKE %s OR marca LIKE %s)
    """
    valor_busqueda = f"%{termino}%"
    cursor.execute(query, (valor_busqueda, valor_busqueda))
    
    resultados = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return resultados


def obtener_venta_completa(id_venta):
    """
    PROPÓSITO: Recupera de forma relacional la cabecera (datos generales) y el 
               detalle (artículos comprados) de una venta específica para su auditoría.

    CODER: Regina.

    PARÁMETROS:  
        :id_venta: (int) Identificador único de la venta a buscar.

    RETORNO: 
        :resultado: (dict o None) Diccionario con llaves 'cabecera' y 'detalles', 
                    o None si la factura no existe en la base de datos.
    """  
    conexion = conectar_bd()
    if not conexion:
        return None
        
    cursor = conexion.cursor(dictionary=True)
    
    # Buscar la cabecera uniendo tablas para traer nombres
    query_cabecera = """
        SELECT v.id_venta, v.fecha, concat(u.nombre, ' ', u.apellido) AS vendedor, fp.forma_pago AS forma_pago
        FROM Venta v
        JOIN Usuario u ON v.id_usuario = u.id_usuario
        JOIN FormaPago fp ON v.id_forma_pago = fp.id_forma_pago
        WHERE v.id_venta = %s
    """
    cursor.execute(query_cabecera, (id_venta,))
    cabecera = cursor.fetchone()
    
    # Si la cabecera no existe, la factura no existe.
    if not cabecera:
        cursor.close()
        conexion.close()
        return None
        
    # Buscar los datos de artículos de esa factura
    query_detalles = """
        SELECT p.descripcion, p.marca, dv.cantidad, dv.precio_unitario, (dv.cantidad * dv.precio_unitario) AS subtotal
        FROM DetalleVenta dv
        JOIN Producto p ON dv.id_producto = p.id_producto
        WHERE dv.id_venta = %s
    """
    cursor.execute(query_detalles, (id_venta,))
    detalles = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return {"cabecera": cabecera, "detalles": detalles}



def registrar_compra_transaccion(id_proveedor, lista_productos):
    """
    PROPÓSITO: Registra una compra a proveedor. Inserta cabecera y detalles.
               El trigger de la BD actualiza el stock automáticamente.
    CODER: Fernanda / Regina.

    Lógica de compras para manejar los cambios de precios: 
    Usamos el modelo de 'Costo de Reposición' onda negocios de retail. 
    En lugar de complicar el código en Python creando lotes separados para cada precio, 
    armamos un Trigger que al registrar una compra, automáticamente hace tres cosas: 
    - suma el nuevo stock al existente, 
    - actualiza el precio de costo del producto al valor de la factura más reciente, 
    - recalcula el precio de venta al público (sumándole un 40% de margen). 
    Así nos aseguramos de que el vendedor siempre facture con el precio actualizado. 
    El historial exacto de cuánto pagamos en el pasado queda guardado en la tabla de detalles 
    de compra (guarda la auditoría! XD)
    """   
    conexion = conectar_bd()
    if not conexion: 
        return False
    
    cursor = conexion.cursor()
    try:
        conexion.start_transaction()
        
        # 1. Insertar Cabecera de Compra (Solo Proveedor y Fecha, acorde al MER)
        cursor.execute("INSERT INTO Compra (id_proveedor, fecha) VALUES (%s, NOW())", 
                       (id_proveedor,))
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_compra = cursor.fetchone()[0]
        
        # 2. Insertar Detalles
        query_detalle = """
            INSERT INTO DetalleCompra (id_compra, id_producto, cantidad, precio_costo) 
            VALUES (%s, %s, %s, %s)
        """
        for prod in lista_productos:
            cursor.execute(query_detalle, (id_compra, prod['id_producto'], prod['cantidad'], prod['precio_costo']))
            
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        print(f"Error crítico en BD al registrar compra: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()


def obtener_productos_stock_critico():
    """
    PROPÓSITO: Recupera el listado de productos en estado crítico desde 
    la vista SQL VW_StockCritico.
    CODER: Regina.
    """   
    conexion = conectar_bd()
    if not conexion:
        return []
        
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM VW_StockCritico")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al consultar stock crítico: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()        


def dar_baja_logica_producto(id_producto):
    """
    PROPÓSITO: Cambia el estado del producto a inactivo.
    CODER: Regina
    """
    from db.connection import conectar_bd
    conexion = conectar_bd()
    if not conexion: 
        return False
    
    cursor = conexion.cursor()
    try:
        # Si no estuviera el PA, sería un 
        # cursor.execute("UPDATE Producto SET activo = 0 WHERE id_producto = %s", (id_producto,))
        cursor.execute("CALL PA_BajaLogicaProducto(%s)", (id_producto,))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexion.rollback()
        print(f"Error al ejecutar baja lógica: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()


def obtener_productos_activos_ordenados():
    from db.connection import conectar_bd
    conexion = conectar_bd()
    if not conexion: return []
    cursor = conexion.cursor(dictionary=True)
    try:
        # Trae solo los activos (activo = 1)
        cursor.execute("SELECT * FROM Producto WHERE activo = 1 ORDER BY precio_venta")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()


def obtener_productos_inactivos():
    """
    PROPÓSITO: Recupera el listado de productos retirados de la venta (activo = 0).
    CODER: Fernanda
    """
    from db.connection import conectar_bd
    conexion = conectar_bd()
    if not conexion: 
        return []
        
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Producto WHERE activo = 0 ORDER BY descripcion")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar productos inactivos: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()


def insertar_producto(descripcion, marca, precio_compra, precio_venta, id_categoria):
    from db.connection import conectar_bd
    conexion = conectar_bd()
    if not conexion: return False
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO Producto (descripcion, marca, precio_compra, precio_venta, id_categoria, stock, activo) 
            VALUES (%s, %s, %s, %s, %s, 0, 1)
        """, (descripcion, marca, precio_compra, precio_venta, id_categoria))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexion.rollback()
        print(f"Error al insertar: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()


def obtener_categorias():
    from db.connection import conectar_bd
    conexion = conectar_bd()
    if not conexion: return []
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_categoria, categoria FROM Categoria ORDER BY categoria")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al traer categorías: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()