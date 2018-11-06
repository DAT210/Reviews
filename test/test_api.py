'''Testing of the RestfulAPI - Flask'''

from .test import Test
import json


class TestApi(Test):

	def test_get_test(self):
		response = self.client.get("/api/1.0/test/")
		self.assertEqual((response.get_json(), response.status_code), ({
			'status': "Success",
			'data': {
				'id': 'test_id',
				'rating': 5,
				'description': "The id test_id has a rating of 5 stars."
			}
		}, 200))

	def test_add(self):
		"""Will the id be added in the given format?"""
		request = json.dumps({
			'data': [
				{'id': "test_01", 'name': "First Test"},
				{'id': "test_02", 'name': "Second Test"}
			]
		})
		response = self.api_add(request)
		self.assertEqual(
			(response.get_json(), response.status_code),
			({'status': "success", 'data': None}, 201))

	def test_add2(self):
		"""Will the id be added in the given format?"""
		request = json.dumps({
			'data': {'id': "test_01", 'name': "First Test"}
		})
		response = self.api_add(request)
		self.assertEqual(
			(response.get_json(), response.status_code),
			({'status': "error"}, 404))

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

	def api_set(self, id, data, content_type='application/json'):
		return self.client.patch(
			"/api/1.0/reviews/", data=data, content_type=content_type,
			follow_redirects=True
		)

	def api_delete(self, id, content_type='application/json'):
		return self.client.delete(f"/api/1.0/reviews/{id}", follow_redirects=True)


if __name__ == '__main__':
	unittest.main()
