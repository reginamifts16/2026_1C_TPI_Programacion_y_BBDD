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
from db.dao import obtener_rendimientos_mensuales, obtener_ventas_agrupadas_por_usuario



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
        # Usamos las claves correctas que devuelve la consulta SQL
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