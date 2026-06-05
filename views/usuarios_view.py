"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: usuarios_view.py
CAPA: Vista (views)
DESCRIPCIÓN:
Pantallas relacionadas con la administración de usuarios.

Estas vistas serán utilizadas exclusivamente por:
- Administrador
===============================================================================
"""

from views.components import *


# =============================================================================
# GESTIÓN DE USUARIOS
# =============================================================================

def mostrar_usuarios(frame):

    crear_pantalla_base(
        frame,
        "Gestión de Usuarios",
        "Alta, modificación, baja lógica y asignación de roles."
    )