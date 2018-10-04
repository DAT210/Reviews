CREATE DATABASE IF NOT EXISTS meal_testdb /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;

USE meal_testdb;

CREATE TABLE IF NOT EXISTS reviews_meal (
  meal_id varchar(10) NOT NULL,
  review double unsigned NOT NULL,
  score int(10) unsigned NOT NULL,
  nr_of_reviews int(10) unsigned NOT NULL,
  PRIMARY KEY (meal_id),
  UNIQUE KEY meal_id_UNIQUE (meal_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

TRUNCATE reviews_meal;

INSERT INTO reviews_meal (meal_id, review, score, nr_of_reviews) VALUES 
  ('m_fs0214', 0, 0, 0),
  ('m_fs0203', 0, 0, 0),
  ('m_fs0205', 0, 0, 0),
  ('m_fs0208', 0, 0, 0),
  ('m_fs0213', 0, 0, 0),
  ('m_fs0221', 0, 0, 0),
  ('m_fs0234', 0, 0, 0),
  ('m_fs02m2', 0, 0, 0),
  ('m_fs02m3', 0, 0 ,0),
  ('m_fs02m4', 0, 0, 0);