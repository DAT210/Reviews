CREATE DATABASE IF NOT EXISTS meal_db /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;

USE meal_db;

CREATE TABLE IF NOT EXISTS reviews_meal (
  meal_id varchar(10) NOT NULL,
  review double unsigned NOT NULL,
  score int(10) unsigned NOT NULL,
  nr_of_reviews int(10) unsigned NOT NULL,
  PRIMARY KEY (meal_id),
  UNIQUE KEY meal_id_UNIQUE (meal_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;