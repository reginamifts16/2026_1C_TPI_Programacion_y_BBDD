# Tecno Store

Sistema de Gestión y Punto de Venta para comercios minoristas de productos tecnológicos.

## Descripción

Tecno Store es una aplicación desarrollada como trabajo práctico integrador para las asignaturas **Técnicas de Programación** y **Administración y Gestión de Bases de Datos** del **IFTS N.º 16**.

El sistema permite administrar las operaciones principales de un negocio de artículos tecnológicos:

- Gestión de productos e inventario.
- Registro de compras a proveedores.
- Registro de ventas.
- Control de stock.
- Administración de usuarios y roles.
- Generación de reportes e indicadores de gestión.

El proyecto fue diseñado utilizando una arquitectura por capas para separar la lógica de negocio, el acceso a datos y la interfaz gráfica.

---

## Objetivos

- Centralizar la información operativa del negocio.
- Mantener la integridad y consistencia de los datos.
- Controlar el acceso según el perfil del usuario.
- Facilitar la gestión de inventario y ventas.
- Obtener información útil para la toma de decisiones.

---

## Funcionalidades

### Gestión de Usuarios

- Alta de usuarios.
- Modificación de usuarios.
- Baja lógica.
- Asignación de roles.

### Gestión de Productos

- Alta de productos.
- Modificación de productos.
- Baja lógica.
- Consulta de stock.

### Gestión de Categorías

- Alta y modificación de categorías.
- Consulta de categorías.

### Gestión de Proveedores

- Alta de proveedores.
- Modificación de proveedores.
- Baja lógica.
- Consulta de proveedores.

### Compras

- Registro de compras.
- Asociación con proveedores.
- Actualización automática de stock.

### Ventas

- Registro de ventas.
- Selección de forma de pago.
- Generación de ticket.
- Descuento automático de stock.

### Reportes

- Rendimientos mensuales.
- Ranking de productos.
- Rendimiento por vendedor.
- Ventas por forma de pago.
- Consultas analíticas.

---

## Roles del Sistema

### Administrador

Acceso completo a todas las funcionalidades.

### Gerente

Acceso a reportes e indicadores de gestión.

### Vendedor

- Registro de ventas.
- Consulta de stock.
- Consulta de productos.

### Depositero

- Gestión de inventario.
- Registro de compras.
- Control de stock.
- Consulta de proveedores.

---

## Arquitectura

El sistema implementa una arquitectura por capas:

```text
tecno_store/
│
├── main.py
├── setup.bat
├── ejecutar.bat
├── requirements.txt
├── readme.txt
├── README.md
│
├── db/
│   ├── connection.py
│   ├── init_db.py
│   └── dao.py
│
├── logic/
│   ├── auth.py
│   ├── inventario.py
│   ├── ventas.py
│   ├── compras.py
│   └── reportes.py
│
├── sql/
│   ├── 01_tecno_store_db.estructura.sql
│   ├── 02_tecno_store_db.cargaData.sql
│   ├── 03_tecno_store_db.consultas.sql
│   ├── 04_tecno_store_db.vistas.sql
│   ├── 05_techno_store_db.procedimientos.sql
│   └── 06_techno_store_db.triggers.sql
│
├── views/
│   ├── login_view.py
│   ├── menu_principal.py
│   ├── ventas_view.py
│   ├── inventario_view.py
│   ├── compras_view.py
│   ├── reportes_view.py
│   └── usuarios_view.py
│
└── utils/
    ├── ticket.py
    └── helpers.py
```

### Capas

| Capa | Responsabilidad |
|--------|--------|
| db | Acceso a datos y consultas SQL |
| logic | Reglas de negocio |
| views | Interfaz gráfica |
| utils | Funciones auxiliares |

---

## Modelo de Datos

Principales entidades del sistema:

- Usuario
- Rol
- Producto
- Categoría
- Proveedor
- Compra
- DetalleCompra
- Venta
- DetalleVenta
- FormaPago

### Relaciones principales

- Un Rol puede estar asignado a muchos Usuarios.
- Un Usuario puede registrar muchas Ventas.
- Una Forma de Pago puede utilizarse en muchas Ventas.
- Un Proveedor puede suministrar muchas Compras.
- Una Compra puede incluir muchos Productos.
- Una Venta puede contener muchos Productos.
- Un Producto pertenece a una Categoría.

---

## Tecnologías Utilizadas

- Python 3.x
- Tkinter
- MySQL
- Git
- GitHub

---

## Principios de Diseño

- Arquitectura por capas.
- Separación de responsabilidades.
- Baja lógica mediante campo `activo`.
- Integridad referencial mediante claves foráneas.
- Uso de transacciones para operaciones críticas.
- Consultas analíticas realizadas en SQL.

---

## Requisitos Previos

- Python 3.x
- MySQL
- Git

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/USUARIO/tecno-store.git
```

Ingresar al proyecto:

```bash
cd tecno-store
```

Crear la base de datos ejecutando el script SQL correspondiente.

Configurar los parámetros de conexión en:

```text
config.py
```

Ejecutar la aplicación:

```bash
python main.py
```

---

## Base de Datos

El proyecto incluye:

- Creación de tablas.
- Restricciones de integridad.
- Claves primarias.
- Claves foráneas.
- Consultas SQL.
- Vistas.
- Procedimientos almacenados.
- Triggers.

---

## Integrantes

| Integrante | Responsabilidad |
|------------|------------|
| Cristian Duszynski | DevOps · Backend · Git |
| María Fernanda Jurado | Integración Frontend · Validaciones · QA · Testing · Documentación |
| Regina Noemí Molares | Arquitectura · Modelado de Datos · DBA · Backend · Scrum Master |
| Jennifer Moyano | QA · Testing · Documentación |

---

## Asignaturas

### Técnicas de Programación

IFTS N.º 16  
Docente: Ingrid García

### Administración y Gestión de Bases de Datos

IFTS N.º 16  
Docente: Lic. Gustavo Escandell

---

## Licencia

Proyecto desarrollado exclusivamente con fines académicos para el IFTS N.º 16.
No destinado a uso comercial.
