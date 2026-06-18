-- /sql/02_tecno_store_db.cargaData.sql
/*SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE DetalleVenta;
TRUNCATE TABLE Venta;
TRUNCATE TABLE DetalleCompra;
TRUNCATE TABLE Compra;
TRUNCATE TABLE Producto;
TRUNCATE TABLE Proveedor;
TRUNCATE TABLE Usuario;
TRUNCATE TABLE FormaPago;
TRUNCATE TABLE Categoria;
TRUNCATE TABLE Rol;
SET FOREIGN_KEY_CHECKS = 1;*/

-- =============================================================================
-- 1. TABLAS MAESTRAS (INSERCIÓN CON ID FIJO)
-- =============================================================================

INSERT INTO Rol (id_rol, rol) VALUES 
(1, 'Admin'),
(2, 'Gerente'),
(3, 'Vendedor'),
(4, 'Depositero');

INSERT INTO Categoria (id_categoria, categoria) VALUES 
(1, 'Almacenamiento'),
(2, 'Procesadores'),
(3, 'Memorias'),
(4, 'Placas de Video'),
(5, 'Periféricos');

INSERT INTO FormaPago (id_forma_pago, forma_pago) VALUES 
(1, 'Efectivo'),
(2, 'Tarjeta de Débito'),
(3, 'Tarjeta de Crédito'),
(4, 'Transferencia Bancaria');

-- =============================================================================
-- 2. TABLA: USUARIO 
-- =============================================================================

INSERT INTO Usuario (apellido, nombre, clave, id_rol, activo) VALUES 
('Duszynski', 'Cristian', 'admin123', 1, 1),
('Molares', 'Regina', 'regi_mgr', 2, 1),
('Moyano', 'Jennifer', 'jenni_dep', 3, 1),
('Jurado', 'Fernanda', 'fer_top', 4, 1),
('Medina', 'Carlos', 'carlos_med', 3, 1),
('Rodríguez', 'Marina', 'marina_low', 3, 1);

-– INSERTS EXTRA PARA NO SUFRIR
INSERT INTO Usuario (apellido, nombre, clave, id_rol, activo) VALUES 
('Admin', 'El', 'admin123', 1, 1), 
('Gerente', 'El', 'gerente123', 2, 1), 
('Vendedor', 'El', 'vendedor123', 3, 1), 


-- =============================================================================
-- 3. TABLA: PROVEEDOR 
-- =============================================================================

INSERT INTO Proveedor (razon_social, telefono, activo) VALUES 
('Logitech Argentina S.A.', '1144445555', 1),
('Kingston LATAM Distribuidora', '1155556666', 1),
('ASUS Mayorista Oficial', '1133334444', 1),
('Intel Componentes del Sur', '1122223333', 1),
('Corsair Distribuciones', '1166667777', 1);

-- =============================================================================
-- 4. TABLA: PRODUCTO 
-- =============================================================================

INSERT INTO Producto (id_categoria, descripcion, marca, precio_compra, precio_venta, stock, activo) VALUES 
(1, 'Disco Sólido SSD 480GB A400', 'Kingston', 25000.00, 38000.00, 80, 1),
(1, 'Disco Sólido SSD 1TB NVME M.2', 'Kingston', 45000.00, 69000.00, 70, 1),
(1, 'Disco Rígido Externo 2TB USB 3.0', 'Seagate', 52000.00, 78000.00, 50, 1),
(1, 'Disco Sólido SSD 2TB NVME Kingston', 'Kingston', 85000.00, 125000.00, 40, 1),
(1, 'Disco Rígido Interno 1TB Barracuda', 'Seagate', 35000.00, 53000.00, 65, 1),
(2, 'Procesador Core i5 12400F LGA1700', 'Intel', 120000.00, 175000.00, 50, 1),
(2, 'Procesador Ryzen 5 5600X AM4', 'AMD', 115000.00, 169000.00, 55, 1),
(2, 'Procesador Ryzen 7 5700X AM4', 'AMD', 170000.00, 245000.00, 40, 1),
(2, 'Procesador Core i3 12100F', 'Intel', 80000.00, 115000.00, 60, 1),
(2, 'Procesador Core i9 14900K', 'Intel', 490000.00, 685000.00, 35, 1), -- Corrección técnica: precio_venta > precio_compra
(3, 'Memoria RAM 8GB DDR4 3200MHz Vengeance', 'Corsair', 18000.00, 28000.00, 100, 1),
(3, 'Memoria RAM 16GB DDR5 5200MHz Dominator', 'Corsair', 38000.00, 59000.00, 80, 1),
(3, 'Memoria RAM Fury 8GB DDR4 Beast', 'Kingston', 17500.00, 26500.00, 95, 1),
(3, 'Memoria RAM Fury 16GB DDR4 Beast', 'Kingston', 32000.00, 48000.00, 85, 1),
(3, 'Memoria RAM 32GB DDR5 Corsair Kit', 'Corsair', 75000.00, 110000.00, 45, 1),
(3, 'Memoria RAM Sodimm 8GB DDR4 Notebook', 'Kingston', 19000.00, 29000.00, 70, 1),
(4, 'Placa de Video RTX 4060 Ti 8GB Dual', 'ASUS', 350000.00, 499000.00, 40, 1),
(4, 'Placa de Video GTX 1650 4GB Phoenix', 'ASUS', 110000.00, 165000.00, 45, 1),
(4, 'Placa de Video RX 7600 XT 16GB', 'ASUS', 320000.00, 460000.00, 35, 1),
(4, 'Placa de Video RX 6600 V2 8GB', 'ASUS', 210000.00, 299000.00, 38, 1),
(4, 'Placa de Video RTX 3050 6GB', 'ASUS', 160000.00, 235000.00, 42, 1),
(5, 'Mouse Óptico Inalámbrico G305', 'Logitech', 22000.00, 34000.00, 100, 1),
(5, 'Auriculares Gamer G435 Wireless', 'Logitech', 55000.00, 85000.00, 65, 1),
(5, 'Mouse Gamer Ergónomico G502 Hero', 'Logitech', 42000.00, 62000.00, 75, 1),
(5, 'Teclado Mecánico Pro X Tournament', 'Logitech', 80000.00, 120000.00, 50, 1),
(5, 'Cámara Web HD C920 Pro Stream', 'Logitech', 62000.00, 93000.00, 55, 1),
-- Casos disparadores de Stock Crítico
(1, 'Disco Sólido SSD 240GB Sata3', 'Kingston', 15000.00, 23000.00, 3, 1),
(2, 'Procesador Core i7 13700K Boxer', 'Intel', 280000.00, 399000.00, 2, 1),
(4, 'Placa de Video RTX 4070 Super 12GB', 'ASUS', 590000.00, 820000.00, 1, 1),
(5, 'Teclado Mecánico G413 Carbon RGB', 'Logitech', 45000.00, 68000.00, 4, 1),
(1, 'Disco Sólido SSD 240GB Sata3', 'Kingston', 15000.00, 23000.00, 3, 1), 
(2, 'Procesador Core i7 13700K Boxer', 'Intel', 280000.00, 399000.00, 2, 1),
(4, 'Placa de Video RTX 4070 Super 12GB', 'ASUS', 590000.00, 820000.00, 1, 1),
(5, 'Teclado Mecánico G413 Carbon RGB', 'Logitech', 45000.00, 68000.00, 4, 1); 

-- =============================================================================
-- 5. TABLA: COMPRA 
-- =============================================================================

INSERT INTO Compra (fecha, id_proveedor) VALUES 
('2026-05-01', 1),
('2026-05-02', 2),
('2026-05-02', 3),
('2026-05-03', 4),
('2026-05-04', 5),
('2026-05-05', 2);

-- =============================================================================
-- 6. TABLA: DETALLECOMPRA
-- =============================================================================

INSERT INTO DetalleCompra (id_compra, id_producto, precio_costo, cantidad) VALUES 
(1, 25, 22000.00, 50),
(1, 26, 45000.00, 30),
(2, 1, 25000.00, 40),
(2, 2, 45000.00, 35),
(3, 19, 350000.00, 20),
(3, 20, 110000.00, 25),
(4, 7, 120000.00, 25),
(4, 8, 280000.00, 20),
(5, 13, 18000.00, 50),
(5, 14, 38000.00, 40),
(6, 15, 17500.00, 50),
(6, 21, 32000.00, 15);

-- =============================================================================
-- 7. TABLA: VENTA 
-- =============================================================================

INSERT INTO Venta (fecha, id_forma_pago, id_usuario) VALUES 
('2026-05-06', 1, 4), ('2026-05-06', 2, 4), ('2026-05-07', 3, 5), ('2026-05-07', 1, 5), ('2026-05-08', 4, 6),
('2026-05-08', 1, 4), ('2026-05-09', 2, 4), ('2026-05-09', 1, 5), ('2026-05-10', 3, 4), ('2026-05-10', 2, 5),
('2026-05-11', 1, 6), ('2026-05-11', 4, 4), ('2026-05-12', 1, 4), ('2026-05-12', 2, 5), ('2026-05-13', 3, 4),
('2026-05-13', 1, 4), ('2026-05-14', 2, 5), ('2026-05-14', 1, 6), ('2026-05-15', 4, 4), ('2026-05-15', 1, 4),
('2026-05-16', 2, 5), ('2026-05-16', 3, 5), ('2026-05-17', 1, 4), ('2026-05-17', 1, 6), ('2026-05-18', 2, 4),
('2026-05-18', 4, 4), ('2026-05-19', 1, 5), ('2026-05-19', 3, 5), ('2026-05-20', 1, 4), ('2026-05-20', 2, 6),
('2026-05-21', 1, 4), ('2026-05-21', 4, 5), ('2026-05-22', 2, 4), ('2026-05-22', 1, 4), ('2026-05-23', 3, 5),
('2026-05-23', 1, 6), ('2026-05-24', 2, 4), ('2026-05-24', 1, 5), ('2026-05-25', 4, 4), ('2026-05-25', 1, 4),
('2026-05-26', 2, 5), ('2026-05-26', 1, 6), ('2026-05-27', 3, 4), ('2026-05-27', 1, 4), ('2026-05-28', 2, 5),
('2026-05-28', 1, 6), ('2026-05-29', 4, 4), ('2026-05-29', 1, 5), ('2026-05-30', 2, 4), ('2026-05-31', 1, 6);

-- =============================================================================
-- 8. TABLA: DETALLEVENTA
-- =============================================================================

INSERT INTO DetalleVenta (id_venta, id_producto, cantidad, precio_unitario) VALUES 
(1, 1, 1, 38000.00), (1, 13, 2, 28000.00), (2, 25, 1, 34000.00), (3, 7, 1, 175000.00), (4, 15, 2, 26500.00), 
(5, 2, 1, 69000.00), (6, 19, 1, 499000.00), (7, 26, 1, 68000.00), (8, 3, 1, 78000.00), (8, 25, 1, 34000.00), 
(9, 9, 1, 169000.00), (10, 14, 1, 59000.00), (11, 4, 1, 23000.00), (12, 27, 1, 85000.00), (13, 1, 1, 38000.00), 
(14, 20, 1, 165000.00), (15, 8, 1, 399000.00), (16, 28, 1, 62000.00), (17, 13, 2, 28000.00), (17, 25, 1, 34000.00), 
(18, 2, 1, 69000.00), (19, 21, 1, 460000.00), (20, 10, 1, 245000.00), (21, 15, 1, 26500.00), (22, 5, 1, 125000.00), 
(23, 29, 1, 120000.00), (24, 6, 1, 53000.00), (25, 16, 1, 48000.00), (26, 22, 1, 820000.00), (27, 11, 1, 115000.00), 
(27, 13, 1, 28000.00), (28, 30, 1, 93000.00), (29, 1, 1, 38000.00), (30, 25, 2, 34000.00), (31, 7, 1, 175000.00), 
(32, 14, 1, 59000.00), (33, 2, 1, 69000.00), (34, 19, 1, 499000.00), (35, 26, 1, 68000.00), (36, 15, 2, 26500.00), 
(37, 3, 1, 78000.00), (38, 9, 1, 169000.00), (38, 27, 1, 85000.00), (39, 20, 1, 165000.00), (40, 4, 1, 23000.00), 
(41, 13, 1, 28000.00), (42, 23, 1, 299000.00), (43, 28, 1, 62000.00), (44, 5, 1, 125000.00), (44, 16, 1, 48000.00), 
(45, 10, 1, 245000.00), (46, 25, 1, 34000.00), (47, 1, 1, 38000.00), (48, 14, 1, 59000.00), (49, 2, 1, 69000.00), 
(49, 26, 1, 68000.00), (50, 19, 1, 499000.00);

