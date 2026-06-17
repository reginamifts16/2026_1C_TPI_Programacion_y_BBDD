-- =============================================================================
-- OBTENER PRODUCTOS VENDIDOS CON TARJ DE CRÉDITO - TECNO STORE
-- Hecho por: Cristian Duszynski
-- =============================================================================

SELECT p.id_producto, p.descripcion, p.marca
FROM Producto p
INNER JOIN DetalleVenta dv ON p.id_producto = dv.id_producto
WHERE dv.id_venta IN (
    SELECT v.id_venta 
    FROM Venta v
    INNER JOIN FormaPago fp ON v.id_forma_pago = fp.id_forma_pago
    WHERE fp.forma_pago = 'Tarjeta de Crédito'
);