'''Common methods of the various test cases.'''

from flask import current_app
from reviews import create_app
from reviews.db import get_db, mysql
import unittest


class Test(unittest.TestCase):
	initialized = False
	client = None
	app = None

	def setUp(self):
		if not self.initialized:
			print(f"\nInitialize API test...")
			self.__class__.initialized = True
			app = create_app('testing')
			app.testing = True
			self.client = app.test_client()
			self.__class__.init_test_db(app)
			app.config['DB_CONFIG']['db'] = 'reviews_test'
			self.__class__.app = app

	def tearDown(self):
		print(f"Shutting down API test...")
		with self.app.app_context():
			db = get_db()
			cursor = db.cursor()
			try:
				cursor.execute("DROP DATABASE reviews_test;")
				db.commit()
			except mysql.connector.Error as err:
				print(str(err))
			finally:
				cursor.close()

	def init_test_db(app):
		"""Initialize Database for testing on localhost."""
		print(f"Initializes test database...")
		with app.app_context():
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
			finally:
				cursor.close()
				app.config['DB_CONFIG']['db'] = 'reviews_test'
				print(f"Test database initialized!")
