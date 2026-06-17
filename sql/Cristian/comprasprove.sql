-- =============================================================================
-- COMPRAS CON PROVEEDOR (razón social) - TECNO STORE
-- Autor: Cristian Duszynski
-- =============================================================================

CREATE PROCEDURE PA_ObtenerComprasConProveedor()
BEGIN
    SELECT 
        c.id_compra AS 'Código Compra',
        c.fecha AS 'Fecha Compra',
        prov.razon_social AS 'Proveedor'
    FROM Compra c
    INNER JOIN Proveedor prov ON c.id_proveedor = prov.id_proveedor;
END //

DELIMITER ;