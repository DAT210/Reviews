SELECT 'INITIALIZING DATABASE...' AS '';

-- Creates a UID function for comments.
CREATE DATABASE IF NOT EXISTS func;
DROP FUNCTION IF EXISTS insta5.next_id;
DELIMITER $$

CREATE FUNCTION func.next_id(input INT) 
RETURNS BIT(64)
deterministic
BEGIN
	DECLARE
		result, our_epoch, seq_id, now_millis BIGINT;
	DECLARE
		test,
		shard_id int;
	SET our_epoch=1314220021721, shard_id=5;
    SELECT input % 1024 INTO seq_id;
    SELECT FLOOR(UNIX_TIMESTAMP() * 1000) INTO now_millis;
    
    SET result = (now_millis - our_epoch) << 23;
    SET result = result | (shard_id << 10);
    SET result = result | (seq_id);
    RETURN result;
END$$

DELIMITER ;

-- Create database if it does not exist:
CREATE DATABASE IF NOT EXISTS reviews_db /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;

-- Use the database:
USE reviews_db;

-- Drop this table of it exists:
DROP TABLE IF EXISTS review_meals;

-- Creates the reviews table for meals:
CREATE TABLE review_meals (
  meal_id varchar(16) NOT NULL,
  rating double unsigned DEFAULT 0,
  score int(10) unsigned DEFAULT 0,
  nr_of_1_ratings int(10) unsigned DEFAULT 0,
  nr_of_2_ratings int(10) unsigned DEFAULT 0,
  nr_of_3_ratings int(10) unsigned DEFAULT 0,
  nr_of_4_ratings int(10) unsigned DEFAULT 0,
  nr_of_5_ratings int(10) unsigned DEFAULT 0,
  nr_of_ratings int(10) unsigned DEFAULT 0,
  PRIMARY KEY (meal_id),
  UNIQUE KEY meal_id_UNIQUE (meal_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Locks and unlocks the meal review table:
LOCK TABLES review_meals WRITE;
UNLOCK TABLES;

DROP TABLE IF EXISTS review_comments;

CREATE TABLE review_comments (
  comment_id BIT(64) NOT NULL,
  meal_id varchar(16) NOT NULL,
  rating int(10) NOT NULL,
  comment varchar(50) NOT NULL,
  PRIMARY KEY (comment_id),
  UNIQUE KEY comment_id_UNIQUE (comment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DELIMITER //
CREATE TRIGGER before_insert
BEFORE INSERT ON review_comments
FOR EACH ROW
BEGIN
	SET NEW.comment_id = func.next_id(NEW.comment_id);
END//
DELIMITER ;

-- Insert a review for the resturant in the review table for meals:
INSERT INTO review_meals (meal_id) VALUES ('resturant_rating');

SELECT 'DATABASE INITIALIZED!' AS '';