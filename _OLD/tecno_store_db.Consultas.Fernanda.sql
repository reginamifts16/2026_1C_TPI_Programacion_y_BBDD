# obtener_productos_activos_ordenados
SELECT id_producto, id_categoria, descripcion, marca, precio_compra, precio_venta, stock
FROM Producto
WHERE activo = 1
ORDER BY precio_venta ASC;

# obtener_usuarios_por_rol
SELECT id_usuario, apellido, nombre, id_rol, activo
FROM Usuario
WHERE id_rol = 3;

# MODIFICADO por Regina -> ahora llama a una vista
# obtener_stock_critico
/*SELECT id_producto, id_categoria, descripcion, marca, precio_venta, stock, activo
FROM Producto
WHERE stock < 5 AND activo = 1;*/
SELECT * FROM VW_StockCritico;


#obtener_proveedores_activos
SELECT id_proveedor, razon_social, telefono
FROM Proveedor
WHERE activo = 1;

# buscar_producto_por_descripcion
SELECT id_producto, id_categoria, descripcion, marca, precio_venta, stock
FROM Producto
WHERE descripcion LIKE '%SSD%';
