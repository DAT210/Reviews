'''Testing of the RestfulAPI - Flask'''

from .api_test_setup import APITest
import json


class TestAPI(APITest):

	def setUp(self):
		self_id = self.__str__().split(" ")[0]

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

	def test_set_200(self):
		"""Will the rating be set for the meal in the given format?"""
		request = json.dumps({'data': {
			'id': "test_set_01", 'rating': 4, 'comment': "First set rated good."}
		})
		response = self.api_set(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json(), {'status': "success", 'data': None})

	def test_set_404(self):
		"""Will a rating of random id be set?"""
		request = json.dumps({'data': {
			'id': "somerandomid", 'rating': 2, 'comment': "This won't go well."}
		})
		response = self.api_set(request)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.get_json()['status'], "error")

	def test_set_400_rating(self):
		"""Will a rating outside of 1 to 5 be set?"""
		request = json.dumps({'data': {
			'id': "test_set_02", 'rating': 0.9, 'comment': "Too low."
		}})
		response = self.api_set(request)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json()['status'], "error")
		request = json.dumps({'data': {
			'id': "test_set_02", 'rating': 5.1, 'comment': "Too high."
		}})
		response = self.api_set(request)
		self.assertEqual(response.status_code, 400)

	def test_set_400_int(self):
		"""Will a rating which is not an int be set?"""
		request = json.dumps({'data': {
			'id': "test_set_03", 'rating': "4", 'comment': "It's not an int."
		}})
		response = self.api_set(request)
		self.assertEqual(response.status_code, 400)

	def test_set_400_key(self):
		"""Will a rating be set if request misses a key or key is misspelled?"""
		request = json.dumps({'data': {
			'id': "test_set_04", 'comment': "Where's my rating?"
		}})
		response = self.api_set(request)
		self.assertEqual(response.status_code, 400)
		request = json.dumps({'data': {
			'id': "test_set_04", 'id': 3, 'comments': "It's not plural..."
		}})
		response = self.api_set(request)
		self.assertEqual(response.status_code, 400)

	def test_get_200(self):
		"""Will information about the given id be retrieved?"""
		response = self.api_get('test_get_01')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json()['status'], "success")

	def test_get_404(self):
		"""Will information about a random id be retrieved?"""
		response = self.api_get('somerandomid')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.get_json()['status'], "error")

	def test_pull_200(self):
		"""Will information about ratings be pulled?"""
		response = self.api_get()
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json()['status'], "success")

	def test_pull_404(self):
		"""What if there are no meals in database?"""
		response = self.api_get()
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.get_json()['status'], "error")

	def test_delete_200(self):
		"""Will the entry of the given id be deleted?"""
		response = self.api_delete('test_delete_01')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json()['status'], "success")

	def test_delete_404(self):
		"""What would happen if a random id is given?"""
		response = self.api_delete('somerandomdeleteid')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.get_json()['status'], "error")
