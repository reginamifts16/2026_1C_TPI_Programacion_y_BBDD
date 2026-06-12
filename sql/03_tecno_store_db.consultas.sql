/* ============================================================================
CONSULTAS SQL - TECNO STORE
Ordenadas según la matriz de consultas de la documentación del TP
============================================================================ */

/* ============================================================================
CONSULTAS BÁSICAS
============================================================================ */

/* 1. Listar todos los productos activos ordenados por precio de venta
Tipo: Básica
Roles: Admin, Vendedor, Depositero
Coder: Fernanda
*/

SELECT id_producto, id_categoria, descripcion, marca, precio_compra, precio_venta, stock
FROM Producto
WHERE activo = 1
ORDER BY precio_venta ASC;

/* 2. Listar usuarios por rol
Tipo: Básica
Roles: Admin
Coder: Fernanda
*/

SELECT id_usuario, apellido, nombre, id_rol, activo
FROM Usuario
WHERE id_rol = 3;

/* 3. Productos con stock por debajo del mínimo
Tipo: Básica
Roles: Admin, Depositero
Coder: Fernanda
*/

SELECT id_producto, id_categoria, descripcion, marca, precio_venta, stock, activo
FROM Producto
WHERE stock < 5 AND activo = 1;

/* 4. Listar todos los proveedores activos
Tipo: Básica
Roles: Admin, Depositero
Coder: Fernanda
*/

SELECT id_proveedor, razon_social, telefono
FROM Proveedor
WHERE activo = 1;

/* 5. Buscar producto por descripción (LIKE)
Tipo: Básica
Roles: Admin, Vendedor, Depositero
Coder: Fernanda
*/

SELECT id_producto, id_categoria, descripcion, marca, precio_venta, stock
FROM Producto
WHERE descripcion LIKE '%SSD%';

/* ============================================================================
CONSULTAS JOIN
============================================================================ */

/* 6. Ventas con nombre del vendedor que las registró
Tipo: JOIN
Roles: Admin, Gerente
Coder: Cristian
PENDIENTE DE ENTREGA
*/

/* 7. Detalle de venta con descripción y precio de cada producto
Tipo: JOIN
Roles: Admin, Vendedor
Coder: Cristian
PENDIENTE DE ENTREGA
*/

/* 8. Compras con nombre del proveedor
Tipo: JOIN
Roles: Admin, Depositero
Coder: Cristian
PENDIENTE DE ENTREGA
*/

/* 9. Productos que nunca fueron comprados a ningún proveedor
Tipo: LEFT JOIN + NULL
Roles: Admin, Depositero
Coder: Cristian
*/

SELECT
p.id_producto AS 'Código',
p.descripcion AS 'Producto No Comprado',
p.marca AS 'Marca',
p.stock AS 'Stock Actual (Inicial)'
FROM Producto p
LEFT JOIN DetalleCompra dc ON p.id_producto = dc.id_producto
WHERE dc.id_compra IS NULL;

/* ============================================================================
CONSULTAS GROUP BY / HAVING
============================================================================ */

/* 10. Total vendido por mes
Tipo: GROUP BY
Roles: Admin, Gerente
Coder: Regina
*/

-- Implementado dentro de VW_RendimientosMensuales

/* 11. Costos del mes (mercadería comprada)
Tipo: GROUP BY
Roles: Admin, Gerente
Coder: Regina
*/

-- Implementado dentro de VW_RendimientosMensuales

/* 12. Ganancia estimada (ventas - costos)
Tipo: GROUP BY
Roles: Admin, Gerente
Coder: Regina
*/

-- Implementado dentro de VW_RendimientosMensuales

/* 13. Producto más vendido por mes
Tipo: GROUP BY
Roles: Admin, Gerente
Coder: Regina
*/

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
JOIN MaximoPorMes mpm
ON vpm.mes = mpm.mes
AND vpm.total_vendido = mpm.max_cantidad;

/* 14. Categoría más vendida
Tipo: GROUP BY
Roles: Admin, Gerente
Coder: Cristian
PENDIENTE DE ENTREGA
*/

/* 15. Cantidad de ventas por mes
Tipo: GROUP BY
Roles: Admin, Gerente
Coder: Regina
*/

SELECT
DATE_FORMAT(fecha, '%Y-%m') AS mes,
COUNT(id_venta) AS total_ventas
FROM Venta
GROUP BY DATE_FORMAT(fecha, '%Y-%m')
ORDER BY mes ASC;

/* 16. Ticket promedio general
Tipo: GROUP BY
Roles: Admin, Gerente
Coder: Regina
*/

SELECT
ROUND(AVG(sub.total_venta), 2) AS ticket_promedio_general
FROM (
SELECT id_venta, SUM(cantidad * precio_unitario) AS total_venta
FROM DetalleVenta
GROUP BY id_venta
) AS sub;

/* 17. Categorías con más de N productos activos
Tipo: GROUP BY + HAVING
Roles: Admin, Depositero
Coder: Regina
*/

SELECT
c.categoria,
COUNT(p.id_producto) AS total_productos_activos
FROM Producto p
JOIN Categoria c ON p.id_categoria = c.id_categoria
WHERE p.activo = 1
GROUP BY c.id_categoria, c.categoria
HAVING COUNT(p.id_producto) > 5;

/* 18. Vendedores con ticket promedio superior a un monto
Tipo: GROUP BY + HAVING
Roles: Admin, Gerente
Coder: Regina
*/

SELECT
u.id_usuario,
CONCAT(u.apellido, ', ', u.nombre) AS vendedor,
ROUND(AVG(totales_ventas.total_ticket), 2) AS ticket_promedio
FROM (
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

/* 19. Proveedores a los que se compró más de N veces
Tipo: GROUP BY + HAVING
Roles: Admin, Depositero
Coder: Regina
*/

SELECT
pr.razon_social,
COUNT(c.id_compra) AS cantidad_compras
FROM Compra c
JOIN Proveedor pr ON c.id_proveedor = pr.id_proveedor
GROUP BY pr.id_proveedor, pr.razon_social
HAVING COUNT(c.id_compra) > 1;

/* ============================================================================
SUBCONSULTAS OBLIGATORIAS
============================================================================ */

/* 20. Producto con el mayor stock actual
Tipo: Subconsulta escalar
Roles: Admin, Depositero
Coder: Regina
*/

SELECT
id_producto,
descripcion,
marca,
stock
FROM Producto
WHERE stock = (SELECT MAX(stock) FROM Producto);

/* 21. Productos vendidos en ventas pagadas con crédito
Tipo: Subconsulta IN
Roles: Admin, Gerente
Coder: Cristian
*/

SELECT p.id_producto, p.descripcion, p.marca
FROM Producto p
INNER JOIN DetalleVenta dv ON p.id_producto = dv.id_producto
WHERE dv.id_venta IN (
SELECT v.id_venta
FROM Venta v
INNER JOIN FormaPago fp
ON v.id_forma_pago = fp.id_forma_pago
WHERE fp.forma_pago = 'Tarjeta de Crédito'
);

/* 22. Vendedores que tienen al menos una venta registrada
Tipo: Subconsulta EXISTS
Roles: Admin, Gerente
Coder: Cristian
PENDIENTE DE ENTREGA
*/

/* 23. Productos cuyo precio supera el promedio de su categoría
Tipo: Subconsulta correlacionada
Roles: Admin, Gerente, Vendedor
Coder: Regina
*/

SELECT
p1.id_producto,
p1.descripcion,
p1.id_categoria,
p1.precio_venta,
(
SELECT ROUND(AVG(p2.precio_venta), 2)
FROM Producto p2
WHERE p2.id_categoria = p1.id_categoria
) AS promedio_categoria
FROM Producto p1
WHERE p1.precio_venta > (
SELECT AVG(p2.precio_venta)
FROM Producto p2
WHERE p2.id_categoria = p1.id_categoria
);
