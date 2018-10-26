DROP PROCEDURE IF EXISTS func.table_id_seq;

DELIMITER //
CREATE PROCEDURE func.table_id_seq(OUT out_value INT)
BEGIN
	SET out_value = (
    SELECT increment 
    FROM func.increment_table
    WHERE table_id='review_comments');
END//
DELIMITER ;