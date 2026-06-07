"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: login_view.py
CAPA: Vista (views)
DESCRIPCIÓN:
Pantalla de inicio de sesión.

Usuarios de demostración:

    admin       / admin123
    vendedor    / vendedor123
    depositero  / depositero123
    gerente     / gerente123

Por ahora no consulta la base de datos.
La autenticación está simulada para facilitar el desarrollo.
Una vez que todo funcione, volar la hardcodeada y la lógica de login pasarla
a logic\auth.py
===============================================================================
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from views.menu_principal import mostrar_menu_principal
from views.components import *


# PROVISORIO
from views.consultas_view import asignar_rol_logueado



USUARIOS_DEMO = {

    "admin": {
        "password": "admin123",
        "nombre": "Administrador",
        "rol": "administrador"
    },

    "vendedor": {
        "password": "vendedor123",
        "nombre": "Vendedor",
        "rol": "vendedor"
    },

    "depositero": {
        "password": "depositero123",
        "nombre": "Depositero",
        "rol": "depositero"
    },

    "gerente": {
        "password": "gerente123",
        "nombre": "Gerente",
        "rol": "gerente"
    }
}


def mostrar_login():

    ventana = tk.Tk()

    ventana.title("Tecno Store")
    ventana.geometry("1366x768")
    ventana.configure(bg=COLOR_FONDO)

    try:
        ventana.state("zoomed")
    except:
        pass

    contenedor = tk.Frame(
        ventana,
        bg=COLOR_PANEL,
        padx=40,
        pady=40
    )

    contenedor.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    tk.Label(
        contenedor,
        text="TECNO STORE",
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO_OSCURO,
        font=("Arial", 22, "bold")
    ).pack(pady=(0, 20))

    tk.Label(
        contenedor,
        text=(
            "Usuarios de prueba:\n\n"
            "admin / admin123\n"
            "gerente / gerente123\n"
            "vendedor / vendedor123\n"
            "depositero / depositero123"
        ),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO_OSCURO,
        justify="left",
        font=("Arial", 9)
    ).pack(pady=(0, 20))

    tk.Label(
        contenedor,
        text="Usuario",
        bg=COLOR_PANEL
    ).pack(anchor="w")

    entry_usuario = tk.Entry(contenedor, width=30)
    entry_usuario.pack(pady=(0, 15))

    tk.Label(
        contenedor,
        text="Contraseña",
        bg=COLOR_PANEL
    ).pack(anchor="w")

    entry_password = tk.Entry(
        contenedor,
        width=30,
        show="*"
    )

    entry_password.pack(pady=(0, 20))

    def validar_login():
        
        usuario = entry_usuario.get().strip()
        password = entry_password.get().strip()

        if usuario not in USUARIOS_DEMO:

            messagebox.showerror(
                "Error",
                "Usuario inexistente."
            )

            return

        if USUARIOS_DEMO[usuario]["password"] != password:

            messagebox.showerror(
                "Error",
                "Contraseña incorrecta."
            )

            return

        usuario_logueado = {
            "nombre": USUARIOS_DEMO[usuario]["nombre"],
            "rol": USUARIOS_DEMO[usuario]["rol"]            
        }        
        asignar_rol_logueado(USUARIOS_DEMO[usuario]["rol"])

        ventana.destroy()

        mostrar_menu_principal(
            usuario_logueado
        )

    

    frame_botones = tk.Frame(
    contenedor,
    bg=COLOR_PANEL
)

    frame_botones.pack(pady=10)

    tk.Button(
        frame_botones,
        text="Ingresar",
        command=validar_login,
        bg=COLOR_BOTON,
        fg="white",
        width=15
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botones,
        text="Salir",
        command=ventana.destroy,
        width=15
    ).pack(side="left", padx=5)

    ventana.mainloop()