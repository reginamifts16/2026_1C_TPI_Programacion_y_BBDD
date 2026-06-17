-- =============================================================================
-- OBTENER VENDEDORES ACTIVOS (al menos una venta) - TECNO STORE
-- Hecho por: Cristian Duszynski
-- =============================================================================

SELECT 
    u.id_usuario,
    u.nombre,
    u.apellido,
    u.id_rol
FROM Usuario u
WHERE EXISTS (
    SELECT 1 
    FROM Venta v 
    WHERE v.id_usuario = u.id_usuario
);