"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: consultas_view.py
CAPA: Vista (views)
DESCRIPCIÓN:
Pantallas de consulta utilizadas por distintos roles.

Estas vistas serán utilizadas principalmente por:
- Gerente
- Vendedor
- Depositero
===============================================================================
"""

from views.components import *


# =============================================================================
# PRODUCTOS SOBRE PROMEDIO DE CATEGORÍA
# =============================================================================

def mostrar_productos_sobre_promedio(frame):

    crear_pantalla_base(
        frame,
        "Productos Sobre el Promedio de la Categoría",
        "Consulta de productos cuyo desempeño supera el promedio "
        "de su categoría."
    )


# =============================================================================
# VENDEDORES ACTIVOS
# =============================================================================

def mostrar_vendedores_activos(frame):

    crear_pantalla_base(
        frame,
        "Vendedores con Ventas Activas",
        "Consulta de vendedores con actividad registrada."
    )


# =============================================================================
# PRODUCTO CON MAYOR STOCK
# =============================================================================

def mostrar_producto_mayor_stock(frame):

    crear_pantalla_base(
        frame,
        "Producto con Mayor Stock",
        "Consulta del producto con mayor disponibilidad en inventario."
    )