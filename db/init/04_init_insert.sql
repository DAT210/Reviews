-- Insert a review for the resturant in the review table for meals:
INSERT INTO reviews_db.review_meals (meal_id) VALUES ('resturant_rating');

-- Insert an icrement table for the review_comments table:
INSERT INTO func.increment_table (table_id) VALUES ('review_comments');

SELECT 'DATABASE INITIALIZED!' AS '';