-- =============================================================================
-- OBTENER DETALLE DE VENTA - TECNO STORE
-- Autor: Cristian Duszynski
-- =============================================================================

-- ACÁ ES DONDE ME HICE QUILOMBO CON EL BENDITO ID DE VENTA jeje
CREATE PROCEDURE PA_ObtenerDetalleVenta(IN p_id_venta INT)
BEGIN
    SELECT 
        dv.id_venta AS 'Nro Venta',
        p.descripcion AS 'Producto',
        p.marca AS 'Marca',
        dv.cantidad AS 'Cantidad',
        dv.precio_unitario AS 'Precio Unitario',
        (dv.cantidad * dv.precio_unitario) AS 'Subtotal'
    FROM DetalleVenta dv
    INNER JOIN Producto p ON dv.id_producto = p.id_producto
    WHERE dv.id_venta = p_id_venta; -- Filtra por el parámetro que entra
END //