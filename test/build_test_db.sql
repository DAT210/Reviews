CREATE DATABASE IF NOT EXISTS reviews_test /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;

USE reviews_test;

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

TRUNCATE review_meals;

INSERT INTO review_meals (meal_id) VALUES 
  ('get_test_1'),
  ('get_test_2'),
  ('set_test_1'),
  ('set_test_2'),
  ('m_fs0213'),
  ('m_fs0221'),
  ('m_fs0234'),
  ('m_fs02m2'),
  ('m_fs02m3'),
  ('m_fs02m4');