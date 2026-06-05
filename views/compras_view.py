"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: compras_view.py
CAPA: Vista (views)
DESCRIPCIÓN:
Pantallas relacionadas con compras y proveedores.

Estas vistas serán utilizadas principalmente por:
- Administrador
- Depositero
===============================================================================
"""

from views.components import *


# =============================================================================
# REGISTRAR COMPRA
# =============================================================================

def mostrar_registrar_compra(frame):

    crear_pantalla_base(
        frame,
        "Registrar Compra",
        "Registro de compras realizadas a proveedores."
    )


# =============================================================================
# PROVEEDORES
# =============================================================================

def mostrar_proveedores(frame):

    crear_pantalla_base(
        frame,
        "Proveedores",
        "Administración y consulta de proveedores."
    )