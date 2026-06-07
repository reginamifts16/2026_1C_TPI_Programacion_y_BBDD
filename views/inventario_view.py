"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: inventario_view.py
CAPA: Vista (views)
DESCRIPCIÓN:
Pantallas relacionadas con inventario y productos.
CODER: Regina
===============================================================================
"""

from views.components import *


# =============================================================================
# GESTIÓN DE PRODUCTOS
# =============================================================================

def mostrar_productos(frame):

    crear_pantalla_base(
        frame,
        "Gestión de Productos",
        "Alta, modificación, baja lógica y consulta de productos."
    )


# =============================================================================
# STOCK CRÍTICO
# =============================================================================

def mostrar_stock_critico(frame):

    crear_pantalla_base(
        frame,
        "Stock Crítico",
        "Consulta de productos con stock por debajo del mínimo."
    )


# =============================================================================
# CATEGORÍAS
# =============================================================================

def mostrar_categorias(frame):

    crear_pantalla_base(
        frame,
        "Categorías",
        "Administración y consulta de categorías de productos."
    )


# =============================================================================
# CONSULTA DE STOCK
# =============================================================================

def mostrar_consulta_stock(frame):

    crear_pantalla_base(
        frame,
        "Consulta de Stock",
        "Consulta rápida de disponibilidad de productos."
    )