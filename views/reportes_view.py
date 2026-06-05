"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: reportes_view.py
CAPA: Vista (views)
DESCRIPCIÓN:
Pantallas relacionadas con reportes y análisis.

Estas vistas serán utilizadas principalmente por:
- Administrador
- Gerente
===============================================================================
"""

from views.components import *


# =============================================================================
# RENDIMIENTOS MENSUALES
# =============================================================================

def mostrar_rendimientos(frame):

    crear_pantalla_base(
        frame,
        "Rendimientos Mensuales",
        "Resumen de ventas, costos, ganancias y ticket promedio."
    )


# =============================================================================
# RANKING DE PRODUCTOS
# =============================================================================

def mostrar_ranking_productos(frame):

    crear_pantalla_base(
        frame,
        "Ranking de Productos",
        "Consulta de los productos con mejor desempeño."
    )


# =============================================================================
# RENDIMIENTO POR VENDEDOR
# =============================================================================

def mostrar_rendimiento_vendedor(frame):

    crear_pantalla_base(
        frame,
        "Rendimiento por Vendedor",
        "Comparación de desempeño entre vendedores."
    )


# =============================================================================
# VENTAS POR FORMA DE PAGO
# =============================================================================

def mostrar_formas_pago(frame):

    crear_pantalla_base(
        frame,
        "Ventas por Forma de Pago",
        "Análisis de ventas según el medio de pago utilizado."
    )