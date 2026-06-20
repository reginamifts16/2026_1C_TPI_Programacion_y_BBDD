"""
===============================================================================
PROYECTO: Tecno Store - Sistema de Gestión y Punto de Venta
MÓDULO: ticket.py
CAPA: Utilidades / Soporte (Utils)
DESCRIPCIÓN:
Estructura y genera el formato de impresión para los comprobantes de venta 
(tickets) en base a los datos de la transacción.
CODER: Jennifer
===============================================================================
"""

import datetime
from utils.helpers import calcular_iva, formatear_moneda

def generar_ticket(carrito, total_final, vendedor_nombre="Cajero"):
    """
    PROPÓSITO: Genera una cadena de texto (ASCII Art) que simula un comprobante 
    para ser mostrado en pantalla o enviado a una impresora térmica.

    CODER: Jennifer.

    PARÁMETROS:  
        :carrito: (list) Lista de diccionarios con los productos de la transacción.
        :total_final: (float) El monto total a cobrar (incluye IVA).
        :vendedor_nombre: (str) Nombre del usuario que realiza la venta.

    RETORNO: 
        :ticket_str: (str) El comprobante formateado y listo para imprimir.
    """
    # Cálculos para el desglose 
    subtotal_sin_iva = total_final / 1.21
    monto_iva = calcular_iva(subtotal_sin_iva)
    
    fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Armado del ticket (40 caracteres de ancho)
    ticket = []
    ticket.append("=" * 40)
    ticket.append("          TECNO STORE S.A.          ")
    ticket.append("=" * 40)
    ticket.append(f"Fecha: {fecha_actual}")
    ticket.append(f"Atendido por: {vendedor_nombre}")
    ticket.append("-" * 40)
    ticket.append("CANT  DESCRIPCIÓN          SUBTOTAL")
    ticket.append("-" * 40)

    # Listar productos
    for item in carrito:
        cant = str(item['cantidad']).ljust(5)
        # Cortamos la descripción si es muy larga para que no rompa el ticket
        desc = item['descripcion'][:18].ljust(18)
        subt_item = float(item['cantidad']) * float(item['precio_unitario'])
        subt_str = formatear_moneda(subt_item).rjust(15)
        
        ticket.append(f"{cant} {desc} {subt_str}")

    # Pie de totales
    ticket.append("-" * 40)
    ticket.append(f"SUBTOTAL:      {formatear_moneda(subtotal_sin_iva).rjust(25)}")
    ticket.append(f"IVA (21%):     {formatear_moneda(monto_iva).rjust(25)}")
    ticket.append("=" * 40)
    ticket.append(f"TOTAL:         {formatear_moneda(total_final).rjust(25)}")
    ticket.append("=" * 40)
    ticket.append("   ¡Gracias por su compra en Tecno Store!   ")
    ticket.append("=" * 40)

    return "\n".join(ticket)