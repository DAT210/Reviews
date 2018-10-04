
from . import db

def set(id, review):
	if 1 > review or review > 5:
		return
	database = db.get_db()
	cursor = database.cursor()
	try:
		sql = "SELECT score, nr_of_reviews FROM reviews_meal WHERE meal_id=%s"
		cursor.execute(sql, (id,))
		(score, nr_of_reviews) = cursor.fetchone()
		score += review
		nr_of_reviews += 1
		review = round((score/nr_of_reviews), 1)
		sql = "UPDATE reviews_meal SET review=%s, score=%s, nr_of_reviews=%s WHERE meal_id=%s"
		cursor.execute(sql, (review, score, nr_of_reviews, id,))
		database.commit()
	except db.mysql.connector.Error as err:
		print(f"Error_set: {err}")
	finally:
		cursor.close()
	return

def get(id):
	database = db.get_db()
	cursor = database.cursor()
	try:
		sql = "SELECT review FROM reviews_meal WHERE meal_id=%s"
		cursor.execute(sql, (id,))
		review = cursor.fetchone()
		if review is not None:
			(review,) = review
		return review
	except db.mysql.connector.Error as err:
		print(f"Error_get: {err}")
	finally:
		cursor.close()
	return

def remove(id):
	database = db.get_db()
	cursor = database.cursor()
	try:
		sql = "DELETE FROM reviews_meal WHERE meal_id=%s"
		cursor.execute(sql, (id,))
		database.commit()
	except db.mysql.connector.Error as err:
		print(f"Error_remove: {err}")
	finally:
		cursor.close()
	return

def add(id):
	database = db.get_db()
	cursor = database.cursor()
	try:
		sql = "INSERT INTO reviews_meal (meal_id, review, score, nr_of_reviews) VALUES (%s, 0, 0, 0)"
		cursor.execute(sql, (id,))
		database.commit()
	except db.mysql.connector.Error as err:
		print(f"Error_add: {err}")
	finally:
		cursor.close()
	return