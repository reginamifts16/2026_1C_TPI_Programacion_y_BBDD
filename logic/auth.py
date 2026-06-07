"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: auth.py
CAPA: Lógica de Negocio (Controlador / Servicios)
DESCRIPCIÓN:
Gestiona la autenticación de usuarios, validación de credenciales, control
de sesiones y verificación de permisos según el rol asignado y estado.
CODER: Regina
===============================================================================
"""

from db.dao import obtener_usuario_por_username

def autenticar_usuario(username_ingresado, clave_ingresada):
    """
    PROPÓSITO: valida credenciales usando username compuesto.

    CODER: Regina.

    PARÁMETROS:  
    	:username_ingresado: (str) Nombre y apellido     	
        :clave_ingresada: (str) Nombre y apellido    

    RETORNO: 
    	:success: (bool), True si login exitoso
        :nombre: (str),  nombre y apellido
        :rol: (str), en minúsculas. 

    """
    # Elimina espacios
    username_limpio = username_ingresado.strip().replace(" ", "")
    
    usuario = obtener_usuario_por_username(username_limpio)
    
    if not usuario:
        return {"error": "Usuario inexistente."}
        
    if usuario["activo"] == 0:
        return {"error": "Usuario inhabilitado para el ingreso."}
        
    if usuario["clave"] != clave_ingresada:
        return {"error": "Contraseña incorrecta."}
    
    rol_final = usuario["rol"].lower()
    if rol_final == "admin":
        rol_final = "administrador"
        
    return {
        "success": True,
        "nombre": f"{usuario['nombre']} {usuario['apellido']}",
        "rol": rol_final
    }