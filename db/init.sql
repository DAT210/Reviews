SELECT 'INITIALIZING DATABASE...' AS '';

-- Create database if it does not exist:
CREATE DATABASE IF NOT EXISTS reviews_db /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;

-- Use the database:
USE reviews_db;

-- Drop this table of it exists:
DROP TABLE IF EXISTS reviews_meal;

-- Creates the reviews table for meals:
CREATE TABLE reviews_meal (
  meal_id varchar(16) NOT NULL,
  review double unsigned NOT NULL,
  score int(10) unsigned NOT NULL,
  nr_of_reviews int(10) unsigned NOT NULL,
  PRIMARY KEY (meal_id),
  UNIQUE KEY meal_id_UNIQUE (meal_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Locks and unlocks the meal review table:
LOCK TABLES reviews_meal WRITE;
UNLOCK TABLES;

-- Insert a review for the resturant in the review table for meals:
INSERT INTO reviews_meal (meal_id, review, score, nr_of_reviews) VALUES 
  ('resturant_review', 0, 0, 0);

SELECT 'DATABASE INITIALIZED!' AS '';