'''Templates for the JSON reponses to an API request.'''


class API_Templates():

	def standard(status, data):
		"""
		Returns a template to be used for json responses to an API request.\n
		The status field is either 'success', 'fail', or 'error'.
		"""

		template = {
			'status': status,
			'data': data
		}
		return template

	def get_data(
		uid, name, rating, one_ratings, two_ratings, three_ratings, four_ratings,
		five_ratings, comments_array=None
	):
		"""
		Returns a template to be used for the json response of a API GET request.
		"""

		if comments_array is None:
			count = 0
		else:
			count = len(comments_array)
		template = {
			'id': uid,
			'name': name,
			'rating': rating,
			'review_rating_counts': {
				'1': one_ratings,
				'2': two_ratings,
				'3': three_ratings,
				'4': four_ratings,
				'5': five_ratings
			},
			'description': f"{name} has a rating of {rating} of 5 stars.",
			'comments_count': count,
			'comments': comments_array
		}
		return template

	def get_datas(uid, name, rating, comments_array=None):
		"""
		Returns a template to be used for the json response of a API GET request.
		"""

		template = {
			'id': uid,
			'name': name,
			'rating': rating,
			'description': f"{name} has a rating of {rating} of 5 stars.",
			'comments': comments_array
		}
		return template

	def comment(rating, comment):
		"""
		Returns a template for a comment in a json response to an API request.
		"""

		template = {
			'rating': rating,
			'comment': comment
		}
		return template
