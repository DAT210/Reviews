-- Create database if it does not exist:
CREATE DATABASE IF NOT EXISTS reviews_db;

-- Drop tables if exist:
DROP TABLE IF EXISTS reviews_db.review_meals;
DROP TABLE IF EXISTS reviews_db.review_comments;
DROP TABLE IF EXISTS func.increment_table;

CREATE TABLE func.increment_table (
  `table_id` varchar(128) NOT NULL,
  `increment` INT DEFAULT 0,
  PRIMARY KEY (`table_id`),
  UNIQUE KEY `main_id_UNIQUE` (`table_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE reviews_db.review_comments (
  comment_id BIT(64) NOT NULL default 0,
  meal_id varchar(16) NOT NULL,
  rating int(10) NOT NULL,
  comment varchar(255) NOT NULL,
  PRIMARY KEY (comment_id, meal_id),
  UNIQUE KEY comment_id_UNIQUE (comment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create before insert trigger for review_comments table.
DELIMITER //
CREATE TRIGGER before_insert
BEFORE INSERT ON reviews_db.review_comments
FOR EACH ROW
BEGIN
	SET new.comment_id = func.next_id();
    UPDATE func.increment_table SET increment = increment + 1 WHERE table_id='review_comments';
END//
DELIMITER ;

-- Creates the reviews table for meals:
CREATE TABLE reviews_db.review_ratings (
  meal_id varchar(16) NOT NULL,
  meal_name varchar(16) NOT NULL,
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