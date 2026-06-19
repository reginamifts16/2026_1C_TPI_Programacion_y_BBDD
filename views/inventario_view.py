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
import tkinter as tk
from tkinter import *
from db.dao import obtener_productos_stock_critico

# =============================================================================
# GESTIÓN DE PRODUCTOS
# =============================================================================

def mostrar_productos(frame):

    crear_pantalla_base(
        frame,
        "Gestión de Productos",
        "Alta, modificación, baja lógica y consulta de productos."
    )


def mostrar_stock_critico(frame):
    """
    PROPÓSITO: Renderiza la pantalla para el perfil Depositero.
               Muestra los artículos que requieren reposición urgente.
    """
    limpiar_frame(frame)
    frame.config(bg=COLOR_FONDO)
    
    crear_titulo(frame, "Alerta de Stock Crítico")
    crear_subtitulo(frame, "Productos con menos de 5 unidades en el inventario.")

    # --- PANEL CENTRAL: TABLA DE STOCK CRÍTICO ---
    panel_datos = tk.LabelFrame(frame, text=" Requieren Reposición Inmediata ", bg=COLOR_FONDO, font=("Arial", 10, "bold"))
    panel_datos.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    columnas = ("ID", "Descripción", "Marca", "Stock Actual")
    tree_stock = ttk.Treeview(panel_datos, columns=columnas, show="headings", height=15)
    
    tree_stock.heading("ID", text="ID")
    tree_stock.column("ID", width=50, anchor=tk.CENTER)
    
    tree_stock.heading("Descripción", text="Descripción")
    tree_stock.column("Descripción", width=250, anchor=tk.W)
    
    tree_stock.heading("Marca", text="Marca")
    tree_stock.column("Marca", width=150, anchor=tk.W)
    
    # Destacamos la columna de stock
    tree_stock.heading("Stock Actual", text="Stock Actual")
    tree_stock.column("Stock Actual", width=100, anchor=tk.CENTER)
    
    tree_stock.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # =========================================================================
    # FUNCIONES INTERNAS
    # =========================================================================
    def cmd_cargar_datos():
        # Limpiar tabla de consultas anteriores
        for row in tree_stock.get_children():
            tree_stock.delete(row)
            
        # Llamar al DAO que consulta la vista SQL
        productos = obtener_productos_stock_critico()
        
        if not productos:
            tree_stock.insert("", tk.END, values=("-", "Inventario en niveles óptimos", "-", "-"))
            return
            
        for p in productos:
            tree_stock.insert("", tk.END, values=(p['id_producto'], p['descripcion'], p['marca'], p['stock']))

    # --- PANEL INFERIOR: ACCIONES ---
    frame_acciones = tk.Frame(frame, bg=COLOR_FONDO)
    frame_acciones.pack(fill=tk.X, padx=20, pady=5)
    
    tk.Button(
        frame_acciones, 
        text="🔄 Actualizar Listado", 
        bg=COLOR_BOTON, 
        fg=COLOR_TEXTO_CLARO, 
        font=("Arial", 10, "bold"),
        command=cmd_cargar_datos
    ).pack(side=tk.RIGHT)

    # Disparo inicial automático al abrir la pantalla
    cmd_cargar_datos()


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