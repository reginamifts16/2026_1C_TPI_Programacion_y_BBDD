"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: menu_principal.py
CAPA: Vista (views)
DESCRIPCIÓN:
Ventana principal del sistema.

Contiene:
- Menú lateral
- Submenús dinámicos según el rol
- Área central de contenido

Todas las pantallas se cargan dentro del frame de contenido.
===============================================================================
"""

import tkinter as tk

from views.components import *

from views.ventas_view import *
from views.inventario_view import *
from views.compras_view import *
from views.reportes_view import *
from views.usuarios_view import *
from views.consultas_view import *


MENU_ROLES = {

    "administrador": {

        "Ventas": [
            ("Nueva venta", mostrar_nueva_venta),
            ("Historial ventas", mostrar_historial_ventas),
            ("Anular venta", mostrar_anular_venta)
        ],

        "Inventario": [
            ("Gestión de productos", mostrar_productos),
            ("Stock crítico", mostrar_stock_critico),
            ("Categorías", mostrar_categorias)
        ],

        "Compras": [
            ("Registrar compra", mostrar_registrar_compra),
            ("Proveedores", mostrar_proveedores)
        ],

        "Reportes": [
            ("Rendimientos mensuales", mostrar_rendimientos),
            ("Ranking de productos", mostrar_ranking_productos),
            ("Rendimiento por vendedor", mostrar_rendimiento_vendedor)
        ],

        "Administración": [
            ("Gestión de usuarios", mostrar_usuarios)
        ]
    },

    "gerente": {

        "Reportes": [
            ("Rendimientos mensuales", mostrar_rendimientos),
            ("Ranking de productos", mostrar_ranking_productos),
            ("Rendimiento por vendedor", mostrar_rendimiento_vendedor),
            ("Ventas por forma de pago", mostrar_formas_pago)
        ],

        "Consultas": [
            ("Productos sobre promedio", mostrar_productos_sobre_promedio),
            ("Vendedores activos", mostrar_vendedores_activos)
        ]
    },

    "vendedor": {

        "Ventas": [
            ("Nueva venta", mostrar_nueva_venta),
            ("Mis ventas del día", mostrar_mis_ventas)
        ],

        "Inventario": [
            ("Consultar stock", mostrar_consulta_stock),
            ("Productos sobre promedio", mostrar_productos_sobre_promedio)
        ]
    },

    "depositero": {

        "Inventario": [
            ("Gestión de productos", mostrar_productos),
            ("Stock crítico", mostrar_stock_critico),
            ("Categorías", mostrar_categorias)
        ],

        "Compras": [
            ("Registrar compra", mostrar_registrar_compra),
            ("Proveedores", mostrar_proveedores)
        ],

        "Consultas": [
            ("Producto con mayor stock", mostrar_producto_mayor_stock)
        ]
    }
}

def cerrar_sesion(ventana):
    ventana.destroy()
    from views.login_view import mostrar_login
    mostrar_login()


def mostrar_dashboard(frame_contenido):

    limpiar_frame(frame_contenido)

    crear_titulo(
        frame_contenido,
        "Bienvenido a Tecno Store"
    )

    crear_subtitulo(
        frame_contenido,
        "Seleccione una opción desde el menú lateral."
    )


def mostrar_submenu(frame_submenu,
                    frame_contenido,
                    rol,
                    menu):

    limpiar_frame(frame_submenu)

    titulo = tk.Label(
        frame_submenu,
        text=menu,
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO_OSCURO,
        font=("Arial", 11, "bold")
    )

    titulo.pack(
        pady=(10, 10)
    )

    opciones = MENU_ROLES[rol][menu]

    for texto, funcion in opciones:

        crear_boton_submenu(
            frame_submenu,
            texto,
            lambda f=funcion: f(frame_contenido)
        )


def mostrar_menu_principal(usuario):

    ventana = tk.Tk()

    ventana.title("Tecno Store")
    ventana.geometry("1366x768")
    ventana.configure(bg=COLOR_FONDO)

    try:
        ventana.state("zoomed")
    except:
        pass

    # ============================================================
    # CONTENEDOR MENÚ LATERAL
    # ============================================================

    frame_menu = tk.Frame(
        ventana,
        bg=COLOR_MENU,
        width=260
    )

    frame_menu.pack(
        side="left",
        fill="y"
    )

    frame_menu.pack_propagate(False)

    # ============================================================
    # ZONA SUPERIOR (LOGO + MENÚ PRINCIPAL)
    # ============================================================

    frame_menu_superior = tk.Frame(
        frame_menu,
        bg=COLOR_MENU
    )

    frame_menu_superior.pack(
        fill="x"
    )

    # ============================================================
    # ÁREA CENTRAL (SUBMENÚ)
    # ============================================================

    frame_submenu = tk.Frame(
        frame_menu,
        bg=COLOR_PANEL
    )

    frame_submenu.pack(
        fill="both",
        expand=True,
        padx=5,
        pady=5
    )

    # ============================================================
    # ÁREA INFERIOR (CERRAR SESIÓN)
    # ============================================================

    frame_inferior = tk.Frame(
        frame_menu,
        bg=COLOR_MENU
    )

    frame_inferior.pack(
        fill="x",
        side="bottom"
    )

    # ============================================================
    # CONTENIDO PRINCIPAL
    # ============================================================

    frame_contenido = tk.Frame(
        ventana,
        bg=COLOR_FONDO
    )

    frame_contenido.pack(
        side="right",
        fill="both",
        expand=True
    )

    # ============================================================
    # CABECERA
    # ============================================================

    tk.Label(
        frame_menu_superior,
        text="TECNO STORE",
        bg=COLOR_MENU,
        fg="white",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        frame_menu_superior,
        text=f"{usuario['nombre']}\n({usuario['rol']})",
        bg=COLOR_MENU,
        fg="white"
    ).pack(pady=(0, 20))

    # ============================================================
    # MENÚ PRINCIPAL
    # ============================================================

    rol = usuario["rol"]

    for menu in MENU_ROLES[rol]:

        crear_boton_menu(
            frame_menu_superior,
            menu,
            lambda m=menu: mostrar_submenu(
                frame_submenu,
                frame_contenido,
                rol,
                m
            )
        )

    # ============================================================
    # BOTÓN CERRAR SESIÓN
    # ============================================================

    tk.Button(
        frame_inferior,
        text="Cerrar sesión",
        command=lambda: cerrar_sesion(ventana),
        bg=COLOR_BOTON,
        fg="white"
    ).pack(
        fill="x",
        padx=10,
        pady=10
    )

    # ============================================================
    # PANTALLA INICIAL
    # ============================================================

    mostrar_dashboard(frame_contenido)

    ventana.mainloop()