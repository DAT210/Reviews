SELECT 'INITIALIZING DATABASE...' AS '';

CREATE DATABASE IF NOT EXISTS func;

DROP FUNCTION IF EXISTS func.next_id;

DELIMITER
CREATE FUNCTION func.next_id()
    RETURNS BIT(64)
    deterministic
BEGIN
	DECLARE
		result, our_epoch, seq_id, now_millis BIGINT;
	DECLARE
		inc, shard_id int;
	SET our_epoch=1314220021721, shard_id=364;
    
    CALL func.table_id_seq(@out_value);
    SELECT @out_value % 1024 INTO seq_id;
    SELECT FLOOR(UNIX_TIMESTAMP() * 1000) INTO now_millis;

    SET result = (now_millis - our_epoch) << 23;
    SET result = result | (shard_id << 10);
    SET result = result | (seq_id);
    RETURN result;
END;
DELIMITER