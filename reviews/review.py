'''The Review portion of the Reviews API'''
import random
from reviews.db import (
	get_db, mysql
)
from flask import current_app


class Rating():
	"""Used for setting, adding, getting, and removing ratings of an object."""

	def set(id, rating):
		"""
		Used for setting a rating in the database,\
		the 'rating' must be an integer.
		"""
		db = get_db()
		cursor = db.cursor()
		try:
			sql = "SELECT score, nr_of_ratings FROM review_ratings WHERE meal_id=%s;"
			cursor.execute(sql, (id,))
			fetch = cursor.fetchone()
			if fetch is None:
				return
			(score, nr_of_ratings,) = fetch
			score += rating
			nr_of_ratings += 1
			rating_f = round((score / nr_of_ratings), 1)
			sql = "UPDATE review_ratings \
				SET rating=%s, score=%s, nr_of_ratings=nr_of_ratings+1 \
				, nr_of_%s_ratings=nr_of_%s_ratings+1 WHERE meal_id=%s;"
			cursor.execute(sql, (rating_f, score, rating, rating, id,))
			set_check = cursor.rowcount
			db.commit()
			return set_check
		except mysql.connector.Error as err:
			return err
		finally:
			cursor.close()
		return

	def get(id):
		db = get_db()
		cursor = db.cursor()
		try:
			cursor.execute("LOCK TABLES review_ratings READ;")
			sql = "SELECT meal_name, rating, nr_of_1_ratings, nr_of_2_ratings,\
				nr_of_3_ratings, nr_of_4_ratings, nr_of_5_ratings\
				FROM review_ratings WHERE meal_id=%s;"
			cursor.execute(sql, (id,))
			result = cursor.fetchone()
			cursor.execute("UNLOCK TABLES;")
			if result is not None:
				(name, rating, rating_1, rating_2, rating_3, rating_4, rating_5,) = result
				result = (name, rating, rating_1, rating_2, rating_3, rating_4, rating_5)
			return result
		except mysql.connector.Error as err:
			return err
		finally:
			cursor.close()
		return

	def pull():
		db = get_db()
		cursor = db.cursor()
		try:
			cursor.execute("LOCK TABLES review_ratings READ;")
			sql = "SELECT meal_id, meal_name, rating FROM review_ratings;"
			cursor.execute(sql,)
			result = cursor.fetchall()
			cursor.execute("UNLOCK TABLES;")
			return result
		except mysql.connector.Error as err:
			print(f"Error_get(): {err}")
		finally:
			cursor.close()
		return

	def remove(id):
		db = get_db()
		cursor = db.cursor()
		try:
			cursor.execute("LOCK TABLES review_ratings WRITE;")
			sql = "DELETE FROM review_ratings WHERE meal_id=%s;"
			cursor.execute(sql, (id,))
			delete_check = cursor.rowcount
			cursor.execute("UNLOCK TABLES;")
			db.commit()
			return delete_check
		except mysql.connector.Error as err:
			return err
		finally:
			cursor.close()
		return

	def add(meals):
		db = get_db()
		cursor = db.cursor()
		insert_check = 0
		try:
			cursor.execute("LOCK TABLES review_ratings WRITE;")
			sql = "INSERT INTO review_ratings (meal_id, meal_name)\
				VALUES (%s, %s);"
			for meal in meals:
				try:
					meal_id = meal.pop('id')
					meal_name = meal.pop('name')
				except KeyError as err:
					return err
				cursor.execute(sql, (meal_id, meal_name,))
				insert_check += cursor.rowcount
			db.commit()
			cursor.execute("UNLOCK TABLES;")
		except mysql.connector.Error as err:
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
			cursor.execute("LOCK TABLES review_comments WRITE;")
			sql = "INSERT INTO review_comments(meal_id, rating, comment) \
				VALUES (%s, %s, %s);"
			cursor.execute(sql, (the_id, rating, comment,))
			check = cursor.rowcount
			db.commit()
			cursor.execute("UNLOCK TABLES;")
			return check
		except mysql.connector.Error as err:
			return err
		finally:
			cursor.close()
		return

	def get(the_id, sort='DESC', offset=0, limit=10):
		"""
		Gets a comment from the database.
		\n'the_id' is the id of the object getting reviewed, and must be set.
		\nThe 'sort' parameter tells the query if it's sorted in ascending\
		or descending order, the default is 'DESC' and the only other value\
		that can be set is 'ASC'.
		\nThe 'offset' parameter tells the query which row should it start at,\
		the default is 0.
		\nThe 'limit' parameter tells the query how many rows it should return, \
		starting at the 'offset'.
		"""
		db = get_db()
		cursor = db.cursor()
		sort = sort.upper()
		if sort != 'ASC' and sort != 'DESC':
			sort = 'DESC'
		try:
			cursor.execute("LOCK TABLES review_comments READ;")
			sql = f"SELECT rating, comment FROM review_comments\
				WHERE meal_id=%s ORDER BY comment_id {sort} LIMIT %s,%s;"
			cursor.execute(sql, (the_id, offset, limit,))
			result = cursor.fetchall()
			cursor.execute("UNLOCK TABLES;")
			return result
		except mysql.connector.Error as err:
			return err
		finally:
			cursor.close()
		return
