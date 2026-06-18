"""
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: init_db.py
CAPA: Acceso a Datos / Infraestructura
DESCRIPCIÓN: Script de inicialización automática (Migración). 
             Garantiza que la base de datos, tablas y rutinas existan 
             antes de que la interfaz gráfica intente consumirlas.
CODER: Regina
"""
import mysql.connector

def inicializar_entorno_bd():
    """
    PROPÓSITO: Se conecta al motor MySQL genérico, crea la base de datos si no existe,
               y compila los Procedimientos Almacenados y Triggers necesarios.
    PARÁMETROS: Ninguno.
    RETORNO: (bool) True si todo se inicializó bien, False si hubo error crítico.
    """
    try:
        # Nos conectamos al motor MySQL, SIN especificar la database aún
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            port=3306
        )
        cursor = conexion.cursor()

        # Crear Base de Datos
        cursor.execute("CREATE DATABASE IF NOT EXISTS tecno_store_db;")
        cursor.execute("USE tecno_store_db;")

        # Compilar el Procedimiento de Venta (¡Sin DELIMITER!)
        # Primero lo borramos por si hicimos algún cambio en el código y queremos que se actualice
        cursor.execute("DROP PROCEDURE IF EXISTS PA_RegistrarVenta;")
        
        query_proc_venta = """
        CREATE PROCEDURE PA_RegistrarVenta(
            IN p_id_forma_pago INT,
            IN p_id_usuario INT
        )
        BEGIN
            INSERT INTO Venta (id_forma_pago, id_usuario)
            VALUES (p_id_forma_pago, p_id_usuario);
        END
        """
        cursor.execute(query_proc_venta)

        # Agregar la creación de los Triggers con la misma lógica:
        # cursor.execute("DROP TRIGGER IF EXISTS TR_DescontarStockVenta;")
        # cursor.execute("CREATE TRIGGER ...")

        conexion.commit()
        print("✓ Entorno de Base de Datos inicializado correctamente.")
        return True

    except Exception as e:
        print(f"❌ Error crítico inicializando la BD: {e}")
        return False
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()