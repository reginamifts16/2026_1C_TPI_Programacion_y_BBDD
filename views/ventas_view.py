"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: ventas_view.py
CAPA: Vista (views)
DESCRIPCIÓN:
Contiene las interfaces gráficas y controladores de eventos para el Punto de 
Venta (POS), Historial de Facturación, Anulaciones y Auditoría Diaria.
Alineado con el estándar transaccional y validación de doble capa.

CODER: Regina
===============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
from views.components import (
    limpiar_frame, 
    validar_entrada_numerica, 
    crear_titulo, 
    crear_subtitulo,
    COLOR_FONDO, 
    COLOR_BOTON, 
    COLOR_TEXTO_CLARO
)
from logic.ventas import calcular_subtotal_memoria, registrar_venta_transaccion
from db.dao import buscar_productos_por_nombre
from utils.ticket import generar_ticket

# =============================================================================
# NUEVA VENTA (PUNTO DE VENTA - POS)
# =============================================================================

def mostrar_nueva_venta(frame, id_usuario_logueado=1):
    """
    PROPÓSITO: Renderiza el Punto de Venta (POS). Maneja el ciclo de búsqueda de productos, 
               armado del carrito en memoria y envío de la transacción a la base de datos.

    CODER: Regina.

    PARÁMETROS:  
        :frame: (tk.Frame) El contenedor principal donde se dibujará la pantalla.
        :id_usuario_logueado: (int) El ID del empleado que está haciendo la venta (para la auditoría).
    """
    limpiar_frame(frame)
    frame.config(bg=COLOR_FONDO)

    # Variable de estado temporal en memoria (Simula estado de POO)
    carrito_actual = [] 

    # =========================================================================
    # FUNCIONES INTERNAS (Controladores de Eventos)
    # =========================================================================
    
    def mostrar_popup_ticket_visual(texto_comprobante):
        """
        PROPÓSITO: Construye una ventana emergente modal que emula la impresión 
                   de un comprobante fiscal en papel térmico con fuentes monoespaciadas.
        """
        ventana_ticket = tk.Toplevel()
        ventana_ticket.title("Comprobante de Venta - Emisión POS")
        ventana_ticket.geometry("380x520")
        ventana_ticket.configure(bg="#ffffff")
        ventana_ticket.resizable(False, False)
        
        # Bloquea la ventana padre de fondo hasta cerrar el popup 
        ventana_ticket.grab_set()

        txt_area = tk.Text(ventana_ticket, font=("Courier New", 10), bd=0, padx=15, pady=15)
        txt_area.insert(tk.END, texto_comprobante)
        txt_area.config(state="disabled") # Bloquea manipulación de texto por el cajero
        txt_area.pack(fill=tk.BOTH, expand=True)

        btn_cerrar = tk.Button(
            ventana_ticket, 
            text="Cerrar e Imprimir", 
            bg=COLOR_BOTON, 
            fg=COLOR_TEXTO_CLARO, 
            font=("Arial", 10, "bold"),
            command=ventana_ticket.destroy
        )
        btn_cerrar.pack(fill=tk.X, padx=20, pady=10)

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
        valores = tree_resultados.item(seleccion[0])['values'] 
        
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
            
        formas_pago_map = {"Efectivo": 1, "Tarjeta de Débito": 2, "Tarjeta de Crédito": 3}
        seleccion_pago = combo_pago.get()
        id_forma_pago = formas_pago_map.get(seleccion_pago, 1)

        total_venta = calcular_subtotal_memoria(carrito_actual)

        # Envío del carro completo a la persistencia transaccional (ACID)
        exito = registrar_venta_transaccion(id_forma_pago, id_usuario_logueado, carrito_actual)
        
        if exito:
            # Emisión del ticket tras confirmación física en BD
            texto_ticket_final = generar_ticket(carrito_actual, total_venta)
            mostrar_popup_ticket_visual(texto_ticket_final)
            
            messagebox.showinfo("Éxito", "Venta registrada y stock descontado exitosamente.")
            mostrar_nueva_venta(frame, id_usuario_logueado) 
        else:
            messagebox.showerror("Error", "Ocurrió un problema en la transacción. Operación abortada.")

    # =========================================================================
    # MAQUETACIÓN 
    # =========================================================================
    tk.Label(frame, text="PUNTO DE VENTA (POS)", font=("Arial", 16, "bold"), bg=COLOR_FONDO).pack(pady=10)

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
    entry_cantidad.insert(0, "1") 
    entry_cantidad.pack(side=tk.LEFT, padx=5)
    tk.Button(frame_agregar, text="Agregar al Carrito ➔", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=cmd_agregar_carrito).pack(side=tk.RIGHT)

    # --- PANEL DERECHO ---
    panel_der = tk.LabelFrame(frame_split, text="2. Carrito de Compras", bg=COLOR_FONDO, font=("Arial", 10, "bold"))
    panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

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

    tk.Button(panel_der, text="💳 CONFIRMAR Y EMITIR TICKET", bg="#2980b9", fg="white", font=("Arial", 12, "bold"), command=cmd_confirmar_venta).pack(fill=tk.X, padx=20, pady=10)


# =============================================================================
# HISTORIAL DE VENTAS
# =============================================================================

def mostrar_historial_ventas(frame):
    """
    PROPÓSITO: Renderiza el historial general de facturas emitidas por la tienda,
               permitiendo auditoría cruzada a los roles Admin y Gerente.

    CODER: Regina.

    PARÁMETROS:  
        :frame: (tk.Frame) El contenedor de interfaz provisto por el menú central.
    """
    limpiar_frame(frame)
    frame.config(bg=COLOR_FONDO)
    
    crear_titulo(frame, "Historial de Ventas")
    crear_subtitulo(frame, "Registro general de comprobantes y auditoría transaccional de la tienda.")

    # Grilla de Visualización
    columnas = ("ID Venta", "Fecha/Hora", "Vendedor", "Forma de Pago", "Monto Total")
    tree_historial = ttk.Treeview(frame, columns=columnas, show="headings", height=12)
    
    for col in columnas:
        tree_historial.heading(col, text=col)
        tree_historial.column(col, width=130, anchor=tk.CENTER)
        
    tree_historial.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)


def mostrar_anular_venta(frame):
    """
    PROPÓSITO: Interfaz gráfica de reversión de operaciones. Permite buscar una factura,
               inspeccionar visualmente sus artículos y montos, y ejecutar la anulación
               atómica con restitución automática de inventario.

    CODER: Regina.

    PARÁMETROS:  
        :frame: (tk.Frame) El contenedor de interfaz provisto por el menú central.
    """
    limpiar_frame(frame)
    frame.config(bg=COLOR_FONDO)
    
    crear_titulo(frame, "Anulación de Comprobantes")
    crear_subtitulo(frame, "Busque la factura por su número de ID e inspeccione los artículos antes de confirmar la baja.")

    # --- PANEL SUPERIOR: BUSCADOR ---
    frame_busqueda = tk.Frame(frame, bg=COLOR_FONDO)
    frame_busqueda.pack(fill=tk.X, padx=20, pady=10)

    tk.Label(frame_busqueda, text="Número de Factura ID:", font=("Arial", 10, "bold"), bg=COLOR_FONDO).pack(side=tk.LEFT)
    entry_id_venta = tk.Entry(frame_busqueda, width=15, font=("Arial", 10, "bold"))
    entry_id_venta.pack(side=tk.LEFT, padx=10)

    # --- PANEL CENTRAL: VISUALIZADOR DE DATOS DE LA OPERACIÓN ---
    panel_datos = tk.LabelFrame(frame, text=" Datos de la Factura Encontrada ", bg=COLOR_FONDO, font=("Arial", 10, "bold"))
    panel_datos.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Etiquetas informativas de cabecera
    frame_info_cabe = tk.Frame(panel_datos, bg=COLOR_FONDO)
    frame_info_cabe.pack(fill=tk.X, padx=10, pady=5)

    lbl_fecha = tk.Label(frame_info_cabe, text="Fecha: --/--/----", bg=COLOR_FONDO, anchor=tk.W)
    lbl_fecha.grid(row=0, column=0, padx=15, pady=2, sticky="w")
    lbl_vendedor = tk.Label(frame_info_cabe, text="Cajero: ----------", bg=COLOR_FONDO, anchor=tk.W)
    lbl_vendedor.grid(row=0, column=1, padx=15, pady=2, sticky="w")
    lbl_pago = tk.Label(frame_info_cabe, text="Forma de Pago: ----------", bg=COLOR_FONDO, anchor=tk.W)
    lbl_pago.grid(row=0, column=2, padx=15, pady=2, sticky="w")

    # Tabla interna para ver los ítems vendidos
    columnas_items = ("Producto", "Marca", "Cantidad", "P. Unitario", "Subtotal")
    tree_items_factura = ttk.Treeview(panel_datos, columns=columnas_items, show="headings", height=6)
    for col in columnas_items:
        tree_items_factura.heading(col, text=col)
        tree_items_factura.column(col, width=100, anchor=tk.CENTER)
    tree_items_factura.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    lbl_total_factura = tk.Label(panel_datos, text="TOTAL FACTURADO: $0.00", font=("Arial", 12, "bold"), bg=COLOR_FONDO, fg="#c0392b")
    lbl_total_factura.pack(pady=5, anchor=tk.E, padx=10)


    # =========================================================================
    # FUNCIONES LOGICAS INTERNAS (Controladores / Clausuras)
    # =========================================================================
    
    def cmd_buscar_factura():
        factura_id_txt = entry_id_venta.get().strip()
        if not validar_entrada_numerica(factura_id_txt):
            messagebox.showerror("Error", "Debe ingresar un número de ID de factura válido.")
            return
            
        # Limpia grilla por las dudas
        for row in tree_items_factura.get_children():
            tree_items_factura.delete(row)
            
        # Llamamos al dao
        from db.dao import obtener_venta_completa
        factura_encontrada = obtener_venta_completa(int(factura_id_txt))
        
        if not factura_encontrada:
            messagebox.showwarning("No Encontrada", f"La Factura #{factura_id_txt} no existe en la base de datos.")
            # Desactivar controles de borrado por seguridad (Escudo anti-falsos positivos)
            lbl_fecha.config(text="Fecha: --/--/----")
            lbl_vendedor.config(text="Cajero: ----------")
            lbl_pago.config(text="Forma de Pago: ----------")
            lbl_total_factura.config(text="TOTAL FACTURADO: $0.00")
            btn_anular.config(state="disabled")
            return
            
        # Si la encuentra -> cargamos la interfaz
        cabe = factura_encontrada['cabecera']
        lbl_fecha.config(text=f"Fecha: {cabe['fecha']}")
        lbl_vendedor.config(text=f"Cajero: {cabe['vendedor']}")
        lbl_pago.config(text=f"Pago: {cabe['forma_pago']}")
        
        total_acumulado = 0.0
        for item in factura_encontrada['detalles']:
            tree_items_factura.insert("", tk.END, values=(
                item['descripcion'], 
                item['marca'], 
                item['cantidad'], 
                f"${item['precio_unitario']}", 
                f"${item['subtotal']}"
            ))
            total_acumulado += float(item['subtotal'])
            
        lbl_total_factura.config(text=f"TOTAL FACTURADO: ${total_acumulado:.2f}")
        
        # Habilitamos el botón de borrado
        btn_anular.config(state="normal")


    def cmd_ejecutar_anulacion():
        factura_id = entry_id_venta.get().strip()
        
        # Doble chequeo de gobernanza operativa
        respuesta = messagebox.askyesno(
            " ATENCIÓN - Confirmar Anulación de la Operación", 
            f"¿Está seguro de que desea eliminar la Factura #{factura_id}?\n\nEsta acción es irreversible: borrará los registros y devolverá los ítems al stock."
        )
        
        if not respuesta:
            return 

        # Invocamos la transacción  
        from logic.ventas import anular_venta_transaccion
        exito, mensaje = anular_venta_transaccion(int(factura_id))

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            # Forzamos una recarga limpia de la pantalla para vaciar los datos borrados
            mostrar_anular_venta(frame)
        else:
            messagebox.showerror("Error de Reversión", mensaje)


    # Asignamos la función de búsqueda al botón de la lupa
    tk.Button(frame_busqueda, text="🔍 Buscar Factura", bg=COLOR_BOTON, fg=COLOR_TEXTO_CLARO, command=cmd_buscar_factura).pack(side=tk.LEFT)

    # --- PANEL INFERIOR: ACCIÓN DE BORRADO ---
    # Inicia deshabilitado por seguridad (state="disabled")
    btn_anular = tk.Button(
        frame, 
        text="CONFIRMAR ANULACIÓN Y REINTEGRAR STOCK", 
        bg="#c0392b", 
        fg="white", 
        font=("Arial", 11, "bold"),
        state="disabled", 
        command=cmd_ejecutar_anulacion
    )
    btn_anular.pack(fill=tk.X, padx=20, pady=15)


# =============================================================================
# MIS VENTAS DEL DÍA
# =============================================================================

def mostrar_mis_ventas(frame):
    """
    PROPÓSITO: Pantalla de arqueo de caja individual para el vendedor en sesión. 
               Muestra el listado filtrado de sus operaciones diarias.

    CODER: Regina.

    PARÁMETROS:  
        :frame: (tk.Frame) El contenedor de interfaz provisto por el menú central.
    """
    limpiar_frame(frame)
    frame.config(bg=COLOR_FONDO)
    
    crear_titulo(frame, "Mis Ventas del Día")
    crear_subtitulo(frame, "Resumen diario personal para arqueo de caja y control de comisiones.")

    # Grilla del Arqueo
    columnas = ("Hora", "Comprobante ID", "Productos", "Monto")
    tree_mis_ventas = ttk.Treeview(frame, columns=columnas, show="headings", height=10)
    
    for col in columnas:
        tree_mis_ventas.heading(col, text=col)
        tree_mis_ventas.column(col, width=140, anchor=tk.CENTER)
        
    tree_mis_ventas.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
    
    lbl_arqueo = tk.Label(frame, text="TOTAL ACUMULADO EN CAJA: $0.00", font=("Arial", 12, "bold"), bg=COLOR_FONDO, fg="#27ae60")
    lbl_arqueo.pack(pady=10, anchor=tk.E, padx=20)