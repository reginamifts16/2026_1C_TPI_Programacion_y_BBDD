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
CODER: Regina
===============================================================================
"""

from views.components import *
import tkinter as tk
from tkinter import ttk, messagebox
from views.components import limpiar_frame, validar_entrada_numerica, COLOR_FONDO, COLOR_BOTON, COLOR_TEXTO_CLARO
from logic.ventas import calcular_subtotal_memoria, registrar_venta_transaccion
from db.dao import buscar_productos_por_nombre


# =============================================================================
# NUEVA VENTA
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from views.components import limpiar_frame, validar_entrada_numerica, COLOR_FONDO, COLOR_BOTON, COLOR_TEXTO_CLARO
from logic.ventas import calcular_subtotal_memoria, registrar_venta_transaccion
from db.dao import buscar_productos_por_nombre

def mostrar_nueva_venta(frame, id_usuario_logueado=1):
    """
    PROPÓSITO: Renderiza el Punto de Venta (POS). Maneja el ciclo de búsqueda de productos, 
               armado del carrito en memoria y envío de la transacción a la base de datos.

    CODER: Regina / Fernanda.

    PARÁMETROS:  
        :frame: (tk.Frame) El contenedor principal donde se dibujará la pantalla.
        :id_usuario_logueado: (int) El ID del empleado que está haciendo la venta (para la auditoría).
    """
    limpiar_frame(frame)
    frame.config(bg=COLOR_FONDO)

 
    carrito_actual = [] 

    # ==========================================
    # FUNCIONES INTERNAS (Controladores de Eventos)
    # ==========================================
    def cmd_buscar():
        termino = entry_buscar.get().strip()
        if not termino:
            messagebox.showwarning("Atención", "Ingrese un producto a buscar.")
            return
            
        resultados = buscar_productos_por_nombre(termino)
        
        # Limpiar grilla izquierda
        for row in tree_resultados.get_children():
            tree_resultados.delete(row)
            
        # Llenar grilla izquierda
        for prod in resultados:
            tree_resultados.insert("", tk.END, text=prod['id_producto'], 
                                   values=(prod['descripcion'], prod['marca'], f"${prod['precio_venta']}", prod['stock']))

    def cmd_agregar_carrito():
        seleccion = tree_resultados.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto de la tabla de resultados.")
            return
            
        cantidad_txt = entry_cantidad.get()
        if not validar_entrada_numerica(cantidad_txt) or int(cantidad_txt) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número entero mayor a cero.")
            return
            
        cantidad = int(cantidad_txt)
        item_id = tree_resultados.item(seleccion[0])['text']
        valores = tree_resultados.item(seleccion[0])['values'] # (Desc, Marca, Precio, Stock)
        
        # Limpiamos el signo $ del precio para los cálculos
        precio_float = float(valores[2].replace("$", ""))
        stock_disponible = int(valores[3])
        
        if cantidad > stock_disponible:
            messagebox.showerror("Stock Insuficiente", f"Solo hay {stock_disponible} unidades disponibles.")
            return
            
        # 1. Agregar a la lista lógica
        nuevo_item = {
            'id_producto': item_id,
            'descripcion': valores[0],
            'cantidad': cantidad,
            'precio_unitario': precio_float
        }
        carrito_actual.append(nuevo_item)
        
        # 2. Reflejar en la grilla visual derecha
        subtotal = cantidad * precio_float
        tree_carrito.insert("", tk.END, values=(valores[0], cantidad, f"${precio_float:.2f}", f"${subtotal:.2f}"))
        
        # 3. Actualizar etiqueta de Totales
        actualizar_total_gui()

    def actualizar_total_gui():
        total = calcular_subtotal_memoria(carrito_actual)
        lbl_total.config(text=f"TOTAL A PAGAR: ${total:.2f}")

    def cmd_confirmar_venta():
        if not carrito_actual:
            messagebox.showwarning("Carrito Vacío", "No hay productos para vender.")
            return
            
        # Diccionario simulado de formas de pago (Esto idealmente viene de la BD)
        formas_pago_map = {"Efectivo": 1, "Tarjeta de Débito": 2, "Tarjeta de Crédito": 3}
        seleccion_pago = combo_pago.get()
        id_forma_pago = formas_pago_map.get(seleccion_pago, 1)

        # Llamada a la capa lógica que creamos con Cristian!
        exito = registrar_venta_transaccion(id_forma_pago, id_usuario_logueado, carrito_actual)
        
        if exito:
            messagebox.showinfo("Éxito", "Venta registrada y stock descontado exitosamente.")
            mostrar_nueva_venta(frame, id_usuario_logueado) # Recarga la pantalla para una nueva venta limpia
        else:
            messagebox.showerror("Error", "Ocurrió un problema en la transacción.")


    # ==========================================
    # MAQUETACIÓN VISUAL (Layout con Grid/Pack)
    # ==========================================
    tk.Label(frame, text="PUNTO DE VENTA (POS)", font=("Arial", 16, "bold"), bg=COLOR_FONDO).pack(pady=10)

    # Contenedor dividido en 2 columnas (Izquierda: Búsqueda, Derecha: Carrito)
    frame_split = tk.Frame(frame, bg=COLOR_FONDO)
    frame_split.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # --- PANEL IZQUIERDO ---
    panel_izq = tk.LabelFrame(frame_split, text="1. Buscar Productos", bg=COLOR_FONDO, font=("Arial", 10, "bold"))
    panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

    frame_busqueda = tk.Frame(panel_izq, bg=COLOR_FONDO)
    frame_busqueda.pack(fill=tk.X, padx=5, pady=5)
    tk.Label(frame_busqueda, text="Nombre/Marca:", bg=COLOR_FONDO).pack(side=tk.LEFT)
    entry_buscar = tk.Entry(frame_busqueda, width=30)
    entry_buscar.pack(side=tk.LEFT, padx=5)
    tk.Button(frame_busqueda, text="🔍 Buscar", bg=COLOR_BOTON, fg=COLOR_TEXTO_CLARO, command=cmd_buscar).pack(side=tk.LEFT)

    # Grilla de Resultados
    columnas_res = ("Desc", "Marca", "Precio", "Stock")
    tree_resultados = ttk.Treeview(panel_izq, columns=columnas_res, show="headings", height=8)
    for col in columnas_res:
        tree_resultados.heading(col, text=col)
        tree_resultados.column(col, width=80)
    tree_resultados.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    frame_agregar = tk.Frame(panel_izq, bg=COLOR_FONDO)
    frame_agregar.pack(fill=tk.X, padx=5, pady=10)
    tk.Label(frame_agregar, text="Cantidad:", bg=COLOR_FONDO).pack(side=tk.LEFT)
    entry_cantidad = tk.Entry(frame_agregar, width=10)
    entry_cantidad.insert(0, "1") # Por defecto 1
    entry_cantidad.pack(side=tk.LEFT, padx=5)
    tk.Button(frame_agregar, text="Agregar al Carrito ➔", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=cmd_agregar_carrito).pack(side=tk.RIGHT)


    # --- PANEL DERECHO ---
    panel_der = tk.LabelFrame(frame_split, text="2. Carrito de Compras", bg=COLOR_FONDO, font=("Arial", 10, "bold"))
    panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

    # Grilla del Carrito
    columnas_cart = ("Desc", "Cant", "P.Unit", "Subtotal")
    tree_carrito = ttk.Treeview(panel_der, columns=columnas_cart, show="headings", height=8)
    for col in columnas_cart:
        tree_carrito.heading(col, text=col)
        tree_carrito.column(col, width=80)
    tree_carrito.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    frame_cobro = tk.Frame(panel_der, bg=COLOR_FONDO)
    frame_cobro.pack(fill=tk.X, padx=5, pady=10)

    tk.Label(frame_cobro, text="Forma de Pago:", bg=COLOR_FONDO).pack(side=tk.LEFT)
    combo_pago = ttk.Combobox(frame_cobro, values=["Efectivo", "Tarjeta de Débito", "Tarjeta de Crédito"], state="readonly", width=15)
    combo_pago.current(0)
    combo_pago.pack(side=tk.LEFT, padx=5)

    lbl_total = tk.Label(frame_cobro, text="TOTAL A PAGAR: $0.00", bg=COLOR_FONDO, font=("Arial", 14, "bold"), fg="#c0392b")
    lbl_total.pack(side=tk.RIGHT, pady=5)

    tk.Button(panel_der, text="💳 CONFIRMAR VENTA", bg="#2980b9", fg="white", font=("Arial", 12, "bold"), command=cmd_confirmar_venta).pack(fill=tk.X, padx=20, pady=10)


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