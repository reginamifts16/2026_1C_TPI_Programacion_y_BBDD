"""
===============================================================================
PROYECTO IFTS16: Tecno Store - Sistema de Gestión y Punto de Venta
AUTORES:
    - Duszynski, Cristian    | Rol: Infraestructura, Backend y Git
    - Jurado, María Fernanda | Rol: Frontend (Tkinter) y Validaciones
    - Molares, Regina Noemí  | Rol: Arquitectura, DBA, Gobernanza IA, Liderazgo
    - Moyano, Jennifer       | Rol: QA, Testing y Documentación
FECHA:    Junio 2026
VERSIÓN:  1.0
PYTHON:   3.x
    
ASIGNATURAS y DOCENTES:
- Técnicas de Programación | DOCENTE:  Ingrid García
- Administración y Gestión de Base de Datos | DOCENTE: Lic. Gustavo Escandell

OBSERVACIÓN:
    Este trabajo práctico se presenta de manera conjunta para ambas asignaturas, 
    contando con la previa autorización de sus respectivos docentes. 
    El desarrollo ha sido concebido bajo un enfoque transversal, con el objetivo 
    de demostrar la integración convergente de los saberes de ambas disciplinas 
    en una solución de software, donde los conceptos teóricos y prácticos 
    de cada materia se potencian mutuamente.
-------------------------------------------------------------------------------
ARCHIVO: main.py
DESCRIPCIÓN:
Punto de entrada principal de la aplicación.

Responsabilidades:
- Iniciar la aplicación.
- Mostrar la pantalla de login.
- Mantener el ciclo principal de Tkinter.

IMPORTANTE:
Toda la navegación comienza en LoginView.
===============================================================================
"""

from views.login_view import mostrar_login


def main():

    mostrar_login()


if __name__ == "__main__":

    main()