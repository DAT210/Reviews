'''The Review portion of the Reviews API'''
import random
from reviews.db import (
	get_db, mysql
)

class Rating():
	"""Used for setting, adding, and getting ratings of an object."""

	def set(id, rating):
		db = get_db()
		cursor = db.cursor()
		try:
			sql = "SELECT score, nr_of_ratings FROM reviews_db.review_meals WHERE meal_id=%s"
			cursor.execute(sql, (id,))
			fetch = cursor.fetchone()
			if fetch is None:
				return
			(score, nr_of_ratings) = fetch
			score += rating
			nr_of_ratings += 1
			rating = round((score/nr_of_ratings), 1)
			sql = "UPDATE reviews_db.review_meals SET rating=%s, score=%s, nr_of_ratings=%s WHERE meal_id=%s"
			cursor.execute(sql, (rating, score, nr_of_ratings, id,))
			set_check = cursor.rowcount
			db.commit()
			return set_check
		except mysql.connector.Error as err:
			print(str(err))
		finally:
			cursor.close()
		return


	def get(id):
		db = get_db()
		cursor = db.cursor()
		try:
			sql = "SELECT rating FROM reviews_db.review_meals WHERE meal_id=%s"
			cursor.execute(sql, (id,))
			rating = cursor.fetchone()
			if rating is not None:
				(rating,) = rating
			return rating
		except mysql.connector.Error as err:
			print(f"Error_get({id}): {err}")
			return err
		finally:
			cursor.close()
		return


	def pull():
		db = get_db()
		cursor = db.cursor()
		try:
			sql = "SELECT meal_id, rating FROM reviews_db.review_meals"
			cursor.execute(sql,)
			return cursor.fetchall()
		except mysql.connector.Error as err:
			print(f"Error_get(): {err}")
		finally:
			cursor.close()
		return


	def remove(id):
		db = get_db()
		cursor = db.cursor()
		try:
			sql = "DELETE FROM reviews_db.review_meals WHERE meal_id=%s"
			cursor.execute(sql, (id,))
			delete_check = cursor.rowcount
			db.commit()
			return delete_check
		except mysql.connector.Error as err:
			print(f"Error_remove: {err}")
			return err
		finally:
			cursor.close()
		return


	def add(meal_ids):
		db = get_db()
		cursor = db.cursor()
		insert_check = 0
		try:
			sql = "INSERT INTO reviews_db.review_meals (meal_id) VALUES (%s);"
			for meal_id in meal_ids:
				cursor.execute(sql, (meal_id,))
				insert_check += cursor.rowcount
			db.commit()
		except mysql.connector.Error as err:
			print(f"Error_add: {err}")
			return err
		finally:
			cursor.close()
		return insert_check


class Comment():
	"""Used for setting and getting comments from the database."""

	def set(the_id, rating, comment):
		"""Sets a comment in the database."""
		db = get_db()
		cursor = db.cursor()
		try:
			sql = "INSERT INTO reviews_db.review_comments (comment_id, meal_id, rating, comment) VALUES (%s, %s, %s, %s);"
			some = random.SystemRandom().getrandbits(16)
			cursor.execute(sql, (some, the_id, rating, comment,))
			db.commit()
			return cursor.rowcount
		except mysql.connector.Error as err:
			return err
		finally:
			cursor.close()
		return

	
	def get(the_id, nr_of_comments=10):
		"""Gets a comment from the database."""
		db = get_db()
		cursor = db.cursor()
		try:
			sql = "SELECT rating, comment FROM reviews_db.review_comments WHERE meal_id=%s ORDER BY comment_id DESC LIMIT %s"
			cursor.execute(sql, (the_id, nr_of_comments,))
			return cursor.fetchall()
		except mysql.connector.Error as err:
			return err
		finally:
			cursor.close()
		return