-- =============================================================================
-- PRODUCTOS NO COMPRADOS - TECNO STORE
-- Autor: Cristian Duszynski
-- =============================================================================

-- Si id_compra es NULL, significa que nunca repusimos ese stock.
SELECT 
    p.id_producto AS 'Código',
    p.descripcion AS 'Producto No Comprado',
    p.marca AS 'Marca',
    p.stock AS 'Stock Actual (Inicial)'
FROM Producto p
LEFT JOIN DetalleCompra dc ON p.id_producto = dc.id_producto
WHERE dc.id_compra IS NULL;