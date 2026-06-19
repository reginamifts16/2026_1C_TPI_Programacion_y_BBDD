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
from db.dao import obtener_productos_stock_critico,obtener_productos_activos_ordenados, obtener_productos_inactivos, obtener_categorias 
from logic.inventario import gestionar_baja_logica, gestionar_alta_producto

# =============================================================================
# GESTIÓN DE PRODUCTOS
# =============================================================================

'''def mostrar_productos(frame):

    crear_pantalla_base(
        frame,
        "Gestión de Productos",
        "Alta, modificación, baja lógica y consulta de productos."
    )'''

# =============================================================================
# MOSTRAR PRODUCTOS CON STOCK BAJO
# =============================================================================
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
# CATEGORÍAS (ESTO VUELA)
# =============================================================================
def mostrar_categorias(frame):

    crear_pantalla_base(
        frame,
        "Categorías",
        "Administración y consulta de categorías de productos."
    )


# =============================================================================
# CONSULTA DE STOCK (YA RESUELTO)
# =============================================================================
def mostrar_consulta_stock(frame):

    crear_pantalla_base(
        frame,
        "Consulta de Stock",
        "Consulta rápida de disponibilidad de productos."
    )


# =============================================================================
# MOSTRAR PRODUCTOS
# =============================================================================
def mostrar_productos(frame):
    """
    PROPÓSITO: Pantalla ABM para el catálogo de productos.
    CODER: Regina / Jennifer
    """
    limpiar_frame(frame)
    frame.config(bg=COLOR_FONDO)
    
    crear_titulo(frame, "Gestión de Catálogo (ABM)")
    crear_subtitulo(frame, "Alta, modificación y baja lógica de productos.")

    frame_split = tk.Frame(frame, bg=COLOR_FONDO)
    frame_split.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # =========================================================================
    # PANEL IZQUIERDO: FORMULARIO
    # =========================================================================
    panel_form = tk.LabelFrame(frame_split, text=" Datos del Producto ", bg=COLOR_FONDO, font=("Arial", 10, "bold"))
    panel_form.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)

    tk.Label(panel_form, text="Descripción:", bg=COLOR_FONDO).pack(anchor=tk.W, padx=10, pady=(10, 0))
    entry_desc = tk.Entry(panel_form, width=30)
    entry_desc.pack(padx=10, pady=2)

    tk.Label(panel_form, text="Marca:", bg=COLOR_FONDO).pack(anchor=tk.W, padx=10, pady=(5, 0))
    entry_marca = tk.Entry(panel_form, width=30)
    entry_marca.pack(padx=10, pady=2)

    tk.Label(panel_form, text="Último Costo $:", bg=COLOR_FONDO).pack(anchor=tk.W, padx=10, pady=(5, 0))
    entry_costo = tk.Entry(panel_form, width=30)
    entry_costo.pack(padx=10, pady=2)

    tk.Label(panel_form, text="Precio Venta $:", bg=COLOR_FONDO).pack(anchor=tk.W, padx=10, pady=(5, 0))
    entry_venta = tk.Entry(panel_form, width=30)
    entry_venta.pack(padx=10, pady=2)

    tk.Label(panel_form, text="Categoría:", bg=COLOR_FONDO).pack(anchor=tk.W, padx=10, pady=(5, 0))
    
    # Carga dinámica del desplegable
    from db.dao import obtener_categorias
    categorias_bd = obtener_categorias()
    lista_cat = [f"{c['id_categoria']} - {c['categoria']}" for c in categorias_bd] if categorias_bd else ["0 - Sin categoría"]
    
    combo_cat = ttk.Combobox(panel_form, values=lista_cat, state="readonly", width=27)
    combo_cat.pack(padx=10, pady=2)
    if lista_cat:
        combo_cat.current(0)

    # Funciones de los botones
    def cmd_guardar():
        desc = entry_desc.get().strip()
        marca = entry_marca.get().strip()
        costo = entry_costo.get().strip()
        venta = entry_venta.get().strip()
        # Extrae solo el número antes del guión
        seleccion_cat = combo_cat.get()
        cat_id = seleccion_cat.split(" - ")[0] if " - " in seleccion_cat else "0"
        
        exito, msj = gestionar_alta_producto(desc, marca, costo, venta, cat_id)
        
        if exito:
            messagebox.showinfo("Éxito", msj)
            cmd_limpiar()
            mostrar_productos(frame) # Recarga la grilla
        else:
            messagebox.showerror("Error", msj)

    def cmd_eliminar():
        seleccion = tree_prod.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto de la lista para eliminar.")
            return
            
        if messagebox.askyesno("Confirmar", "¿Está seguro de retirar este producto de la venta? (Baja Lógica)"):
            item_id = int(tree_prod.item(seleccion[0])['values'][0])
            
            # Invocamos la regla de negocio
            exito, mensaje = gestionar_baja_logica(item_id)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                tree_prod.delete(seleccion[0]) # Lo quitamos de la vista
            else:
                messagebox.showerror("Error", mensaje)

    def cmd_limpiar():
        for entry in (entry_desc, entry_marca, entry_costo, entry_venta, entry_cat):
            entry.delete(0, tk.END)

    frame_btns = tk.Frame(panel_form, bg=COLOR_FONDO)
    frame_btns.pack(pady=20)
    
    tk.Button(frame_btns, text="💾 Guardar", bg="#27ae60", fg="white", width=12, command=cmd_guardar).grid(row=0, column=0, padx=2, pady=2)
    tk.Button(frame_btns, text="🧹 Limpiar", bg="#f39c12", fg="white", width=12, command=cmd_limpiar).grid(row=0, column=1, padx=2, pady=2)
    tk.Button(frame_btns, text="🗑️ Retirar de la venta", bg="#c0392b", fg="white", width=25, command=cmd_eliminar).grid(row=1, column=0, columnspan=2, padx=2, pady=5)

    # =========================================================================
    # PANEL DERECHO: CATÁLOGO ACTIVO
    # =========================================================================
    panel_grilla = tk.LabelFrame(frame_split, text=" Catálogo Activo ", bg=COLOR_FONDO, font=("Arial", 10, "bold"))
    panel_grilla.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

    columnas = ("ID", "Desc", "Marca", "Costo", "Venta", "Stock")
    tree_prod = ttk.Treeview(panel_grilla, columns=columnas, show="headings", height=15)
    
    tree_prod.heading("ID", text="ID")
    tree_prod.column("ID", width=40)
    for col in columnas[1:]:
        tree_prod.heading(col, text=col)
        tree_prod.column(col, width=80)
        
    tree_prod.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Cargar la grilla con db.dao.obtener_productos_activos_ordenados()    
    productos_bd = obtener_productos_activos_ordenados()
    
    for p in productos_bd:
        tree_prod.insert("", tk.END, 
                         values=(p['id_producto'], p['descripcion'], p['marca'], f"${p['precio_compra']}", f"${p['precio_venta']}", p['stock']))
        

# =============================================================================
#  MOSTRAR PRODUCTOS INACTIVOS 
# =============================================================================
def mostrar_productos_inactivos(frame):
    """
    PROPÓSITO: Pantalla de productos retirados de circulación.
    CODER: Regina
    """
    from db.dao import obtener_productos_inactivos
    
    limpiar_frame(frame)
    frame.config(bg=COLOR_FONDO)
    
    crear_titulo(frame, "Auditoría de Catálogo Inactivo")
    crear_subtitulo(frame, "Productos que fueron dados de baja y ya no están a la venta.")

    panel_grilla = tk.LabelFrame(frame, text=" Historial de Productos Discontinuados ", bg=COLOR_FONDO, font=("Arial", 10, "bold"))
    panel_grilla.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

    columnas = ("ID", "Desc", "Marca", "Último Costo", "Stock Remanente")
    tree_inactivos = ttk.Treeview(panel_grilla, columns=columnas, show="headings", height=15)
    
    tree_inactivos.heading("ID", text="ID")
    tree_inactivos.column("ID", width=40)
    for col in columnas[1:]:
        tree_inactivos.heading(col, text=col)
        tree_inactivos.column(col, width=120)
        
    tree_inactivos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    productos_bd = obtener_productos_inactivos()
    
    for p in productos_bd:
        tree_inactivos.insert("", tk.END, values=(
            p['id_producto'], 
            p['descripcion'], 
            p['marca'], 
            f"${p['precio_compra']}", 
            p['stock']
        ))