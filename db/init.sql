SELECT 'INITIALIZING DATABASE...' AS '';

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

-- Insert a review for the resturant in the review table for meals:
INSERT INTO review_meals (meal_id) VALUES ('resturant_rating');

SELECT 'DATABASE INITIALIZED!' AS '';