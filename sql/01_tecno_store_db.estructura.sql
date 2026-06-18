/* 
=======================================================================
CREACIÓN DE BASE DE DATOS Y TABLAS - TECNO STORE
=======================================================================
*/
-- 1. Crear y usar la Base de Datos
CREATE DATABASE IF NOT EXISTS tecno_store_db; 
USE tecno_store_db; 

-- 2. Eliminar tablas previas en orden inverso para evitar conflictos de FK
-- 1. Primero las tablas intermedias (dependen de ventas, compras y productos)
DROP TABLE IF EXISTS DetalleVenta; 
DROP TABLE IF EXISTS DetalleCompra;

-- 2. Luego las tablas dependientes de segundo nivel (dependen de usuarios, proveedores y formas de pago)
DROP TABLE IF EXISTS Venta; 
DROP TABLE IF EXISTS Compra;

-- 3. Después las tablas dependientes de primer nivel (dependen de categorías y roles)
DROP TABLE IF EXISTS Producto; 
DROP TABLE IF EXISTS Usuario; 

-- 4. Por último, las tablas maestras o independientes
DROP TABLE IF EXISTS Proveedor;
DROP TABLE IF EXISTS FormaPago; 
DROP TABLE IF EXISTS Rol; 
DROP TABLE IF EXISTS Categoria;
/* 
=======================================================================
TABLAS MAESTRAS (INDEPENDIENTES) 
=======================================================================
*/
CREATE TABLE IF NOT EXISTS Categoria ( 
    id_categoria INT PRIMARY KEY AUTO_INCREMENT, 
    categoria VARCHAR(50) NOT NULL 
);

CREATE TABLE IF NOT EXISTS Rol (
    id_rol INT PRIMARY KEY AUTO_INCREMENT, 
    rol VARCHAR(30) NOT NULL UNIQUE -- Se agrega UNIQUE según diseño
);

CREATE TABLE IF NOT EXISTS FormaPago ( 
    id_forma_pago INT PRIMARY KEY AUTO_INCREMENT, 
    forma_pago VARCHAR(30) NOT NULL UNIQUE -- Se agrega UNIQUE según diseño
);

CREATE TABLE IF NOT EXISTS Proveedor (
    id_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    razon_social VARCHAR(50) NOT NULL,
    telefono VARCHAR(20),
    activo TINYINT(1) DEFAULT 1 NOT NULL
);

/* 
=======================================================================
TABLAS DEPENDIENTES (CON CLAVES FORÁNEAS)
=======================================================================
*/
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT, 
    apellido VARCHAR(50) NOT NULL,
    nombre VARCHAR(50) NOT NULL, 
    -- Se corrige a VARCHAR(255) y se agrega el CHECK del diseño para soportar Hash futuro
    clave VARCHAR(255) NOT NULL CHECK (CHAR_LENGTH(clave) >= 4), 
    id_rol INT NOT NULL, 
    activo TINYINT(1) DEFAULT 1 NOT NULL, -- Baja lógica
    FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
);

CREATE TABLE IF NOT EXISTS  Producto (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    id_categoria INT NOT NULL,
    descripcion VARCHAR(100) NOT NULL, 
    marca VARCHAR(50) NOT NULL, 
    precio_compra DECIMAL(10,2) NOT NULL CHECK (precio_compra > 0), 
    precio_venta DECIMAL(10,2) NOT NULL CHECK (precio_venta > precio_compra), 
    stock INT NOT NULL DEFAULT 0, 
    activo TINYINT(1) DEFAULT 1 NOT NULL, 
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria) 
);

CREATE TABLE IF NOT EXISTS Venta ( 
    id_venta INT PRIMARY KEY AUTO_INCREMENT, 
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP, 
    id_forma_pago INT NOT NULL, 
    id_usuario INT NOT NULL, 
    FOREIGN KEY (id_forma_pago) REFERENCES FormaPago(id_forma_pago), 
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
); 

CREATE TABLE IF NOT EXISTS Compra (
    id_compra INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_proveedor INT NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor)
);

/*
=======================================================================
 TABLAS INTERMEDIAS (CON CLAVE COMPUESTA)
 =======================================================================
*/

CREATE TABLE IF NOT EXISTS DetalleVenta ( 
    id_venta INT NOT NULL, 
    id_producto INT NOT NULL, 
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario >= 0), 
    PRIMARY KEY (id_venta, id_producto), -- Clave primaria compuesta 
    FOREIGN KEY (id_venta) REFERENCES Venta(id_venta), 
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto) 
); 

CREATE TABLE IF NOT EXISTS DetalleCompra (
    id_compra INT NOT NULL,
    id_producto INT NOT NULL,
    precio_costo DECIMAL(10,2) NOT NULL CHECK (precio_costo > 0),
    cantidad INT NOT NULL CHECK (cantidad > 0),
    PRIMARY KEY (id_compra, id_producto),
    FOREIGN KEY (id_compra) REFERENCES Compra(id_compra),
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto)
);
