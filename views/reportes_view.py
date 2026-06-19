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
from db.dao import obtener_rendimientos_mensuales, obtener_ventas_agrupadas_por_usuario, obtener_rendimiento_vendedores
from utils.helpers import formatear_moneda



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
# RENDIMIENTO POR VENDEDOR (GERENCIA)
# =============================================================================
def mostrar_rendimiento_vendedor(frame):
    from views.components import limpiar_frame, crear_titulo, crear_subtitulo, COLOR_FONDO
    from db.dao import obtener_rendimiento_vendedores
    import tkinter as tk
    from tkinter import ttk

    limpiar_frame(frame)
    crear_titulo(frame, "Rendimiento por Vendedor")
    crear_subtitulo(frame, "Análisis mensual de ventas, costos operativos y margen de ganancia neto.")

    # Armo las columnas del reporte
    columnas = ("Mes", "Vendedor", "Total Vendido", "Costo Mercadería", "Margen de Ganancia")
    tree = ttk.Treeview(frame, columns=columnas, show="headings", height=15)
    
    # Lo pongo besho
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=150)
    tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

    # traigo data del dao
    datos_rendimiento = obtener_rendimiento_vendedores()
    
    # Llena la tabla en bonito
    for fila in datos_rendimiento:
        tree.insert("", tk.END, values=(
            fila['mes'],
            fila['vendedor'],
            formatear_moneda(fila['total_vendido']),   # pa'eso les hice el jelper
            formatear_moneda(fila['costo_total']),     
            formatear_moneda(fila['margen_ganancia'])
        ))


# =============================================================================
# MIS VENTAS 
# =============================================================================
def mostrar_mis_ventas(frame, usuario_logueado):        
    limpiar_frame(frame)
    crear_titulo(frame, f"Historial de Ventas: {usuario_logueado['nombre']}")
    crear_subtitulo(frame, "Listado de tus operaciones registradas por mes.")

    columnas = ("Fecha", "Monto Total")
    tree = ttk.Treeview(frame, columns=columnas, show="headings", height=15)
    
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)
    tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

    historial = obtener_ventas_agrupadas_por_usuario(usuario_logueado['nombre'])
    
    total_acumulado = 0
    for h in historial:
        # acá es donde había roto        
        tree.insert("", tk.END, values=(
            h['mes_anio'],
            f"${h['total_mes']:,.2f}"
        ))
        total_acumulado += h['total_mes']
    
    lbl_total = tk.Label(frame, text=f"TOTAL ACUMULADO VENDIDO: ${total_acumulado:,.2f}", 
                         font=("Arial", 12, "bold"), bg=COLOR_FONDO, fg="#27ae60")
    lbl_total.pack(pady=10, anchor=tk.E, padx=20)


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