'''Testing of the RestfulAPI - Flask'''

import unittest
import requests
from reviews import create_app

class TestApi(unittest.TestCase):
	initialized = False
	client = None

	def setUp(self):
		if not self.initialized:
			print(f"\nInitialize API test...")
			self.__class__.initialized = True
			app = create_app({
				'DB_CONFIG': {
					'host': 'localhost',
					'port': 3306,
					'user': 'root',
					'pswrd': 'root',
					'db': 'reviews_test'
				},
				'DEBUG': True
			})
			app.testing = True
			self.client = app.test_client()

	def tearDown(self):
		print(f"Shutting down API test...")

	def test_get(self):
		respons = self.client.get("http://localhost:3000/api/1.0/test/")
		self.assertEqual((respons.get_json(), respons.status_code), ({
			'status': "Success",
			'data': {
				'id': 'test_id',
				'rating': 5,
				'description': "The id test_id has a rating of 5 stars."
			}
		}, 200))

if __name__ == '__main__':
	unittest.main()