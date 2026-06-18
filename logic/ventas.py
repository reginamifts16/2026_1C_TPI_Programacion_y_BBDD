"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: ventas.py
CAPA: Lógica de Negocio (Controlador / Servicios)
DESCRIPCIÓN:
Controla el flujo transaccional del punto de venta: registro de operaciones, 
cálculo de totales, desglose de detalles y afectación directa al stock.
CODER ZERO: Regina
===============================================================================
"""
from db.connection import conectar_bd

def registrar_venta_transaccion(id_forma_pago, id_usuario, carrito):
    """
    PROPÓSITO: Controla el flujo atómico transaccional de una venta al público. Almacena 
               la cabecera en BD, itera los detalles y asegura el comportamiento ACID global.

    CODER: Regina.

    PARÁMETROS:  
        :id_forma_pago: (int) ID del método de pago seleccionado por el cliente.
        :id_usuario: (int) ID del vendedor/usuario en sesión que procesa el POS.
        :carrito: (list) Lista de diccionarios con estructura:
                  [{'id_producto': int, 'cantidad': int, 'precio_unitario': float}, ...]

    RETORNO: 
        :exito: (bool), True si la cabecera, todos los detalles y las reglas de negocio de stock 
                se confirmaron mediante Commit. False si ocurrió un Rollback por error operativo.
    """
    conexion = conectar_bd()
    if not conexion:
        return False

    cursor = conexion.cursor()
    
    try:
        conexion.start_transaction()

        # 1. Ejecutar procedimiento para cabecera de Venta
        cursor.execute("CALL PA_RegistrarVenta(%s, %s)", (id_forma_pago, id_usuario))
        
        # Recuperar ID autoincremental generado para asociar los detalles
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_venta = cursor.fetchone()[0]

        # 2. Insertar transaccionalmente los ítems del carrito
        query_detalle = """
            INSERT INTO DetalleVenta (id_venta, id_producto, cantidad, precio_unitario) 
            VALUES (%s, %s, %s, %s)
        """
        
        for item in carrito:
            cursor.execute(query_detalle, (
                id_venta, 
                item['id_producto'], 
                item['cantidad'], 
                item['precio_unitario']
            ))

        # 3. Confirmación atómica de cambios en la base de datos
        conexion.commit()
        exito = True

    except Exception as e:
        conexion.rollback()
        print(f"Error en la transacción de venta: {e}")
        exito = False
        
    finally:
        cursor.close()
        conexion.close()

    return exito

def calcular_subtotal_memoria(carrito):
    """
    PROPÓSITO: Recorre la lista temporal del carrito y calcula el monto total a cobrar 
               multiplicando cantidades por precios unitarios.

    CODER: Regina.

    PARÁMETROS:  
        :carrito: (list) Lista de diccionarios de la transacción actual.

    RETORNO: 
        :total: (float) La sumatoria de todos los subtotales de los ítems.
    """
    total = 0.0
    for item in carrito:
        total += float(item['cantidad']) * float(item['precio_unitario'])
    return total