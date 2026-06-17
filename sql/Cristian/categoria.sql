-- =============================================================================
-- OBTENER CATEGORÍA MÁS VENDIDA- TECNO STORE
-- Hecho por: Cristian Duszynski
-- =============================================================================

SELECT 
    c.id_categoria, 
    c.categoria AS 'Categoría', 
    SUM(dv.cantidad) AS 'Total Unidades Vendidas'
FROM DetalleVenta dv
INNER JOIN Producto p ON dv.id_producto = p.id_producto
INNER JOIN Categoria c ON p.id_categoria = c.id_categoria
GROUP BY c.id_categoria, c.categoria
ORDER BY SUM(dv.cantidad) DESC
LIMIT 1;