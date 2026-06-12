/* ============================================================================
   VW_StockCritico
   3. Productos activos con stock menor a 5 unidades
   Roles: Admin, Depositero
   Coder: Fernanda
   ========================================================================= */

CREATE OR REPLACE VIEW VW_StockCritico AS
SELECT
    id_producto,
    id_categoria,
    descripcion,
    marca,
    precio_venta,
    stock,
    activo
FROM Producto
WHERE stock < 5
  AND activo = 1;

/* ============================================================================
   VW_RendimientosMensuales
   11. Costos del mes (mercadería comprada)
   12. Ganancia estimada (ventas - costos)
   13. Producto más vendido por mes*/
   Roles: Admin, Gerente
   Coder: Regina
   ========================================================================= */

CREATE OR REPLACE VIEW VW_RendimientosMensuales AS
WITH TotalVentas AS (
    -- Agrupación de ventas por mes
    SELECT 
        DATE_FORMAT(v.fecha, '%Y-%m') AS mes,
        SUM(dv.cantidad * dv.precio_unitario) AS total_vendido
    FROM Venta v
    JOIN DetalleVenta dv ON v.id_venta = dv.id_venta
    GROUP BY DATE_FORMAT(v.fecha, '%Y-%m')
),
TotalCostos AS (
    -- Agrupación de compras por mes
    SELECT 
        DATE_FORMAT(c.fecha, '%Y-%m') AS mes,
        SUM(dc.cantidad * dc.precio_costo) AS total_costos
    FROM Compra c
    JOIN DetalleCompra dc ON c.id_compra = dc.id_compra
    GROUP BY DATE_FORMAT(c.fecha, '%Y-%m')
)
-- Consolidación final con LEFT JOIN que los meses con ventas se muestren 
-- aunque no hayan tenido compras 
SELECT 
    v.mes,
    ROUND(v.total_vendido, 2) AS total_vendido,
    ROUND(IFNULL(c.total_costos, 0.00), 2) AS total_costos,
    ROUND(v.total_vendido - IFNULL(c.total_costos, 0.00), 2) AS ganancia_estimada
FROM TotalVentas v
LEFT JOIN TotalCostos c ON v.mes = c.mes
ORDER BY v.mes ASC;