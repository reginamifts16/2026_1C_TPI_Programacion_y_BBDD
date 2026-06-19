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
CODER: Regina
===============================================================================
"""

from views.components import *
from db.dao import obtener_rendimientos_mensuales


# =============================================================================
# RENDIMIENTOS MENSUALES
# =============================================================================

'''def mostrar_rendimientos(frame):

    crear_pantalla_base(
        frame,
        "Rendimientos Mensuales",
        "Resumen de ventas, costos, ganancias y ticket promedio."
    )'''


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
# VENTAS POR FORMA DE PAGO (LO DEJAMOS?)
# =============================================================================

def mostrar_formas_pago(frame):

    crear_pantalla_base(
        frame,
        "Ventas por Forma de Pago",
        "Análisis de ventas según el medio de pago utilizado."
    )


# =============================================================================
# RENDIMIENTOS MENSUALES
# =============================================================================
def mostrar_rendimientos(frame):
    limpiar_frame(frame)
    crear_titulo(frame, "Estado de Resultados Mensual")
    
    panel = tk.LabelFrame(frame, text=" Indicadores Financieros ", bg=COLOR_FONDO)
    panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    columnas = ("Mes", "Ventas", "Costos", "Ganancia")
    tree = ttk.Treeview(panel, columns=columnas, show="headings")
    
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    datos = obtener_rendimientos_mensuales()
    for d in datos:
        tree.insert("", tk.END, values=(
            d['mes'], 
            f"${d['total_vendido']:,.2f}", 
            f"${d['total_costos']:,.2f}", 
            f"${d['ganancia_estimada']:,.2f}"
        ))