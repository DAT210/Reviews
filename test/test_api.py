'''Testing of the RestfulAPI - Flask'''

from .api_test_setup import APITest
import json


class TestAPI(APITest):

	def test_get_test(self):
		response = self.client.get("/api/1.0/test/")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json(), {
			'status': "Success",
			'data': {
				'id': 'test_id',
				'rating': 5,
				'description': "The id test_id has a rating of 5 stars."
			}
		})

	def test_404(self):
		"""Will a request to wrong url return a not found?"""
		response = self.client.get("/nonexist/hello/")
		self.assertEqual(response.status_code, 404)

	def test_add_201(self):
		"""Will the id be added in the given format?"""
		request = json.dumps({
			'data': [
				{'id': "test_01", 'name': "First Test"},
				{'id': "test_02", 'name': "Second Test"}
			]
		})
		response = self.api_add(request)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.get_json(), {'status': "success", 'data': None})

	def test_add_400(self):
		"""Will the id be added in the given format?"""
		request = json.dumps({
			'data': {'id': "test_01", 'name': "First Test"}
		})
		response = self.api_add(request)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json()['status'], "error")

	def test_add_409(self):
		"""Will the new meals be added in the given format?"""
		request = json.dumps({
			'data': [{'di': "test_01", 'name': "First Test"}]
		})
		response = self.api_add(request)
		self.assertEqual(response.status_code, 409)
		self.assertEqual(response.get_json()['status'], "error")
