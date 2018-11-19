'''Setup class for API tests.'''

from flask import current_app
from reviews import create_app
from reviews.db import get_db, mysql
import unittest
import logging

# A dict of test cases
test_cases = {
	'reviews': [
		("id", "name"),
	],
	'comments': [
		("id", "rating", "comment"),
	]
}


class APITest(unittest.TestCase):
	initialized = False

	@classmethod
	def setUpClass(cls):
		cls.app = create_app('testing')
		cls.app_context = cls.app.app_context()
		cls.client = cls.app.test_client()
		cls.init_test_db()

	@classmethod
	def tearDownClass(cls):
		print(f"Shutting down API test...")
		with cls.app_context:
			db = get_db()
			cursor = db.cursor()
			try:
				cursor.execute("DROP DATABASE IF EXISTS reviews_test;")
				db.commit()
			except mysql.connector.Error as err:
				print(str(err))
			finally:
				cursor.close()

	@classmethod
	def init_test_db(cls):
		"""Initialize Database for testing on localhost."""
		print(f"Initializes test database...")
		with cls.app_context:
			db = get_db()
			cursor = db.cursor()
			try:
				with current_app.open_resource('../db/test/build_test_db.sql') as f:
					statements = f.read().decode('utf8')
					for statement in statements.split(';'):
						cursor.execute(statement)
				db.commit()
			except mysql.connector.Error as err:
				print(f"Failed initializing test database...")
				print(f"Error_testDBbuild: {err}")
			else:
				print(f"Test database initialized!")
			finally:
				cursor.close()
				cls.app.config['DB_CONFIG']['database'] = 'reviews_test'

	def api_add(self, data, content_type='application/json'):
		return self.client.post(
			"/api/1.0/reviews/", data=data, follow_redirects=True,
			content_type='application/json'
		)

	def api_get(self, id=None):
		url = "api/1.0/reviews/"
		if id is not None:
			url = f"api/1.0/reviews/{id}"
		return self.client.get(url, follow_redirects=True)

	def api_set(self, data, id=None, content_type='application/json'):
		return self.client.patch(
			"/api/1.0/reviews/", data=data, content_type=content_type,
			follow_redirects=True
		)

	def api_delete(self, id, content_type='application/json'):
		return self.client.delete(f"/api/1.0/reviews/{id}", follow_redirects=True)
