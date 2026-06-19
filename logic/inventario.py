"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: inventario.py
CAPA: Lógica de Negocio (Controlador / Servicios)
DESCRIPCIÓN:
Administra las reglas de negocio del inventario: alta/baja lógica de productos,
actualización de stock físico y control de alertas para stock crítico.
CODER ZERO: Regina
===============================================================================
"""

from db.dao import dar_baja_logica_producto, insertar_producto


# =============================================================================
# QUITA DE LA VENTA UN PRODUCTO
# =============================================================================
def gestionar_baja_logica(id_producto):
    """
    PROPÓSITO: Retira un artículo de comercialización (activo = 0).
    CASO DE USO: Un lote de placas de video presenta riesgo de incendio. 
                 Se frena la venta, pero el stock físico aguarda devolución al proveedor.
    """
    if not isinstance(id_producto, int) or id_producto <= 0:
        return False, "ID de producto inválido. Operación cancelada."
        
    exito = dar_baja_logica_producto(id_producto)
    
    if exito:
        return True, "Producto retirado de comercialización (Baja Lógica aplicada)."
    else:
        return False, "Fallo en la base de datos o el producto no existe."
    

# =============================================================================
# ALTA DE NUEVO PRODUCTO 
# =============================================================================
def gestionar_alta_producto(desc, marca, costo_txt, venta_txt, cat_txt):
    if not desc or not marca:
        return False, "La descripción y la marca son obligatorias."
    try:
        costo = float(costo_txt)
        venta = float(venta_txt)
        id_cat = int(cat_txt)
    except ValueError:
        return False, "Los precios deben ser numéricos y la categoría un número entero."
    if costo <= 0 or venta <= 0:
        return False, "Los precios deben ser mayores a cero."
    if venta <= costo:
        return False, "El precio de venta debe superar al costo para generar rentabilidad."
    
    exito = insertar_producto(desc, marca, costo, venta, id_cat)
    return (True, "Producto registrado. Stock inicial: 0.") if exito else (False, "Error en la base de datos.")