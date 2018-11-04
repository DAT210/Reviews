/* Creates a test database, and uses it. */
CREATE DATABASE IF NOT EXISTS reviews_test /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;

USE reviews_test;

/* Creates a table for comments if it does not exists, and truncates it. */
CREATE TABLE IF NOT EXISTS review_comments (
  comment_id INT unsigned NOT NULL AUTO_INCREMENT,
  meal_id varchar(16) NOT NULL,
  rating int(10) NOT NULL,
  comment varchar(255) NOT NULL,
  PRIMARY KEY (comment_id, meal_id),
  UNIQUE KEY comment_id_UNIQUE (comment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

TRUNCATE review_comments;

/* Creates a table for ratings if it does not exists, and truncates it. */
CREATE TABLE IF NOT EXISTS review_ratings (
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

TRUNCATE review_ratings;