-- =============================================================================
-- OBTENER VENTAS CON VENDEDOR - TECNO STORE
-- Hecho por: Cristian Duszynski
-- ==============================================================

DELIMITER //
CREATE PROCEDURE PA_ObtenerVentasConVendedor()
BEGIN
    SELECT 
        v.id_venta AS 'Factura',
        v.fecha AS 'Fecha Venta',
        u.nombre AS 'Nombre Vendedor',
        u.apellido AS 'Apellido Vendedor'
    FROM Venta v
    INNER JOIN Usuario u ON v.id_usuario = u.id_usuario;
END //