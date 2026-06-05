"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: ventas_view.py
CAPA: Vista (views)
DESCRIPCIÓN:
Pantallas relacionadas con ventas.

Por ahora son esqueletos visuales.
Los botones muestran un mensaje temporal para que el equipo
pueda concentrarse primero en la navegación.
===============================================================================
"""

from views.components import *


# =============================================================================
# NUEVA VENTA
# =============================================================================

def mostrar_nueva_venta(frame):

    crear_pantalla_base(
        frame,
        "Nueva Venta",
        "Registro de una nueva venta."
    )


# =============================================================================
# HISTORIAL DE VENTAS
# =============================================================================

def mostrar_historial_ventas(frame):

    crear_pantalla_base(
        frame,
        "Historial de Ventas",
        "Consulta de ventas registradas."
    )


# =============================================================================
# ANULAR VENTA
# =============================================================================

def mostrar_anular_venta(frame):

    crear_pantalla_base(
        frame,
        "Anular Venta",
        "Permite cancelar una venta existente."
    )


# =============================================================================
# MIS VENTAS DEL DÍA
# =============================================================================

def mostrar_mis_ventas(frame):

    crear_pantalla_base(
        frame,
        "Mis Ventas del Día",
        "Consulta de ventas realizadas por el usuario actual."
    )