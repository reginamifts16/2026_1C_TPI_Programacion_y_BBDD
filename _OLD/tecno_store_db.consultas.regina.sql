-- 10. Total vendido por mes (GROUP BY)
-- 11. Costos del mes (mercadería comprada) (GROUP BY)
-- 12. Ganancia estimada (ventas - costos) (GROUP BY)
-- Roles: admin, gerente
-- Coder: Regina

-- Centralicé en una vista
-- para Ganancia estimada (ventas - costos) mensual, 
-- la vista consolida los totales de ambas operaciones 
-- en una estructura unificada por período (Año-Mes).

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

-- en python
-- Para consumo general
-- cursor.execute("SELECT * FROM VW_RendimientosMensuales")

-- Filtrando un mes específico
-- cursor.execute("SELECT * FROM VW_RendimientosMensuales WHERE mes = %s", (mes_buscado,))

-- ------------------------------
-- ---     TESTS PARCIALES    ---
-- ------------------------------
/*
-- 1. Ventas en mayo 2026
SELECT 
    DATE_FORMAT(v.fecha, '%Y-%m') AS mes,
    SUM(dv.cantidad * dv.precio_unitario) AS total_vendido
FROM Venta v
JOIN DetalleVenta dv ON v.id_venta = dv.id_venta
GROUP BY DATE_FORMAT(v.fecha, '%Y-%m');

-- 2. Costos en mayo 2026
SELECT 
    DATE_FORMAT(c.fecha, '%Y-%m') AS mes,
    SUM(dc.cantidad * dc.precio_costo) AS total_costos
FROM Compra c
JOIN DetalleCompra dc ON c.id_compra = dc.id_compra
GROUP BY DATE_FORMAT(c.fecha, '%Y-%m');

-- 3. Ejecutar la vista
SELECT * FROM VW_RendimientosMensuales;

-- ------------------------------
-- --- FIN DE TESTS PARCIALES ---
-- ------------------------------
*/

    

-- 13. Producto más vendido por mes (GROUP BY) - Vista Común Expresión (CTE).
-- Roles: admin, gerente
-- Coder: Regina

WITH VentasPorMes AS (
    SELECT 
        DATE_FORMAT(v.fecha, '%Y-%m') AS mes,
        p.id_producto,
        p.descripcion,
        SUM(dv.cantidad) AS total_vendido
    FROM DetalleVenta dv
    JOIN Venta v ON dv.id_venta = v.id_venta
    JOIN Producto p ON dv.id_producto = p.id_producto
    GROUP BY DATE_FORMAT(v.fecha, '%Y-%m'), p.id_producto, p.descripcion
),
MaximoPorMes AS (
    SELECT mes, MAX(total_vendido) AS max_cantidad
    FROM VentasPorMes
    GROUP BY mes
)
SELECT vpm.mes, vpm.descripcion, vpm.total_vendido
FROM VentasPorMes vpm
JOIN MaximoPorMes mpm ON vpm.mes = mpm.mes AND vpm.total_vendido = mpm.max_cantidad;



-- 15. Cantidad de ventas por mes (GROUP BY)
-- Roles: admin, gerente
-- Coder: Regina

SELECT 
    DATE_FORMAT(fecha, '%Y-%m') AS mes,
    COUNT(id_venta) AS total_ventas
FROM Venta
GROUP BY DATE_FORMAT(fecha, '%Y-%m')
ORDER BY mes ASC;



-- 16. Ticket promedio general (GROUP BY)
-- Roles: admin, gerente
-- Coder: Regina
-- Como el total de cada venta física está atomizado en la tabla DetalleVenta 
-- (cantidad x precio), primero agrupo para obtener el total por cada id_venta 
-- y después calculé el promedio de esos resultados.

SELECT 
    ROUND(AVG(sub.total_venta), 2) AS ticket_promedio_general
FROM (
    SELECT id_venta, SUM(cantidad * precio_unitario) AS total_venta
    FROM DetalleVenta
    GROUP BY id_venta
) AS sub;



-- 17. Categorías con más de 5 productos activos (GROUP BY + HAVING)
-- Roles: admin, depositero
-- Coder: Regina

SELECT 
    c.categoria,
    COUNT(p.id_producto) AS total_productos_activos
FROM Producto p
JOIN Categoria c ON p.id_categoria = c.id_categoria
WHERE p.activo = 1
GROUP BY c.id_categoria, c.categoria
HAVING COUNT(p.id_producto) > 5;



-- 18. Vendedores con ticket promedio superior a un monto (GROUP BY + HAVING)
-- Ejemplo probado con monto de $50,000. 
-- Filtré por rol para asegurarme de que eran vendedores.
-- Roles: admin, gerente
-- Coder: Regina

SELECT 
    u.id_usuario,
    CONCAT(u.apellido, ', ', u.nombre) AS vendedor,
    ROUND(AVG(totales_ventas.total_ticket), 2) AS ticket_promedio
FROM (
    -- Subconsulta para calcular el total bruto de cada venta
    SELECT id_venta, SUM(cantidad * precio_unitario) AS total_ticket
    FROM DetalleVenta
    GROUP BY id_venta
) AS totales_ventas
JOIN Venta v ON totales_ventas.id_venta = v.id_venta
JOIN Usuario u ON v.id_usuario = u.id_usuario
JOIN Rol r ON u.id_rol = r.id_rol
WHERE r.rol = 'Vendedor'
GROUP BY u.id_usuario, u.apellido, u.nombre
HAVING ticket_promedio > 50000.00; 



-- 19. Proveedores frecuentes (GROUP BY + HAVING)
-- Roles: admin, depositero
-- Coder: Regina

SELECT 
    pr.razon_social,
    COUNT(c.id_compra) AS cantidad_compras
FROM Compra c
JOIN Proveedor pr ON c.id_proveedor = pr.id_proveedor
GROUP BY pr.id_proveedor, pr.razon_social
HAVING COUNT(c.id_compra) > 1; -- aumentar cuando crezca la db



-- 20. Producto con el mayor stock actual (Subconsulta escalar)
-- Roles: admin, depositero
-- Coder: Regina

SELECT 
    id_producto, 
    descripcion, 
    marca, 
    stock 
FROM Producto 
WHERE stock = (SELECT MAX(stock) FROM Producto);



-- 23. Productos cuyo precio supera el promedio de su categoría (Subconsulta correlacionada)
-- Roles: admin, gerente, vendedor
-- Coder: Regina

SELECT 
    p1.id_producto, 
    p1.descripcion, 
    p1.id_categoria, 
    p1.precio_venta,
    -- Se incluye el promedio como referencia visual
    (SELECT ROUND(AVG(p2.precio_venta), 2) 
     FROM Producto p2 
     WHERE p2.id_categoria = p1.id_categoria) AS promedio_categoria
FROM Producto p1
WHERE p1.precio_venta > (
    SELECT AVG(p2.precio_venta) 
    FROM Producto p2 
    WHERE p2.id_categoria = p1.id_categoria
);
