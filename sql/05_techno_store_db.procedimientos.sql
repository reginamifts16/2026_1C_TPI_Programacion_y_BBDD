/* ============================================================================
   Procedimiento 1: PA_RegistrarVenta
   Coder: Regina
   ========================================================================= */
DELIMITER $$

CREATE PROCEDURE PA_RegistrarVenta(
    IN p_id_forma_pago INT,
    IN p_id_usuario INT
)
BEGIN

    INSERT INTO Venta (
        id_forma_pago,
        id_usuario
    )
    VALUES (
        p_id_forma_pago,
        p_id_usuario
    );

    SELECT LAST_INSERT_ID() AS id_venta_generada;

END$$

DELIMITER ;

-- 

   /* ============================================================================
   Procedimiento 2: PA_BajaLogicaProducto
   Coder: Regina
   ========================================================================= */