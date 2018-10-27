'''The API portion of the reviews application. Handles API requests.'''

from flask import (
	Flask, g, jsonify, make_response, request, Blueprint
)
from reviews.review import (
	Rating, Comment
)
from reviews.exceptions import APIError

bp = Blueprint('api',__name__,url_prefix='/api/1.0')

# Blueprints:
@bp.route('/test/', methods=['GET'])
def test():
	reply = {
		'status': "Success",
		'data': {
			'id': 'test_id',
			'rating': 5,
			'description': "The id test_id has a rating of 5 stars."
		}
	}
	
	return make_response(jsonify(reply)), 200


@bp.route('/reviews/<string:meal_id>/', methods=['GET'])
@bp.route('/reviews/<string:meal_id>', methods=['GET'])
def get_review(meal_id):
	limit = request.args.get('limit', default=10, type=int)
	sort = request.args.get('sort', default='DESC', type=str)
	offset = request.args.get('offset', default=0, type=int)

	rating = Rating.get(meal_id)
	if rating is None:
		raise APIError(f"The rating for id '{meal_id}' could not be found", status_code=404, type='Not Found')
	elif rating is isinstance(rating, Exception):
		raise APIError(str(rating), status_code=400)

	comments = Comment.get(meal_id, sort=sort, offset=offset, limit=limit)
	if comments is None or isinstance(comments, Exception):
		comments_reply = None
	else:
		comments_reply = []
		for (rating, comment,) in comments:
			comments_reply.append({
				'rating': rating,
				'comment': comment
			})

	reply = {
		'status': 'success',
		'data': {
			'review': {
				'id': meal_id,
				'rating': rating,
				'description': f"The id {meal_id} has a rating of {rating} stars.",
				'comments': comments_reply
			}
		}
	}	

	return make_response(jsonify(reply)), 200


@bp.route('/reviews/', methods=['GET'])
def get_reviews():
	reviews = Rating.pull()
	if reviews is None:
		raise APIError("There are no reviews.", status_code=404, type='Not Found')

	reply = {
		'status': 'success',
		'data': { 'reviews': [] }
	}

	replies = reply['data']['reviews']
	for meal_id, rating in reviews:
		comments = Comment.get(meal_id)
		if comments is None or isinstance(comments, Exception):
			comments_reply = None
		else:
			comments_reply = []
			for (rating, comment,) in comments:
				comments_reply.append({
				'rating': rating,
				'comment': comment
			})

		replies.append({
			'id': meal_id,
			'rating': rating,
			'description': f"The id {meal_id} has a rating of {rating} stars.",
			'comments': comments_reply
		})

	return make_response(jsonify(reply)), 200


@bp.route('/reviews/', methods=['PATCH'])
def set_review():
	if not request.is_json:
		raise APIError("The request must be in json format.", status_code=400, type='Bad Request')

	if not 'data' in request.get_json():
		raise APIError("The json request is not correctly formatted,"
			+ "missing 'data', see the documentation.", status_code=400, type='Bad Request')

	data = request.get_json()['data']
	try:
		meal_id = data.pop('id')
		rating = data.pop('rating')
		comment = data.pop('comment')
	except KeyError as err:
		raise APIError(f"The key {err} could not be found, check documentation for correct request format."
			, status_code=400, type='Bad Request')

	if not isinstance(rating, int):
		raise APIError("The rating must be an integer.", status_code=400, type='Bad Request')

	if rating < 1 or rating > 5:
		raise APIError(f"The rating can't be greater than 5, or less than 1, was {rating}.", 
			status_code=400, type='Bad Request')

	check = Rating.set(meal_id, rating)
	if check is None:
		raise APIError(f"The ID '{meal_id}' does not exist.", status_code=404, type='Not Found')

	check = Comment.set(meal_id, rating, comment) # TODO: Must fix, rating can't be set if comment can't be set.
	if isinstance(check, Exception):
		raise APIError(check, status_code=404, type='Not Found')
	reply = {
		'status': 'success',
		'data': None
	}

	return make_response(jsonify(reply)), 200


@bp.route('/reviews/', methods=['POST'])
def add_review():
	if not request.is_json:
		raise APIError("The request must be in json format.", status_code=400, type='Bad Request')

	if not 'data' in request.get_json():
		raise APIError("The json request is missing 'data', " +
			"read the documentation for the correct format.", status_code=400, type='Bad Request')

	check = Rating.add(request.get_json()['data'])
	if isinstance(check, Exception):
		raise APIError(str(check), status_code=409, type='Conflict')

	reply = {
		'status': 'success',
		'data': None
	}

	return make_response(jsonify(reply)), 201


@bp.route('/reviews/<string:meal_id>/', methods=['DELETE'])
def remove_review(meal_id):
	check = Rating.remove(meal_id)
	if isinstance(check, Exception):
		raise APIError(str(check), status_code=404, type='Not Found')
	elif check is 0:
		raise APIError(f"The ID '{meal_id}' could not be found.", status_code=404, type='Not Found')

	reply = {
		'status': "success",
		'data': None
		}

	return make_response(jsonify(reply)), 200


# Error handling:
@bp.errorhandler(APIError)
def handle_APIError(error):
	return make_response(error.json()), error.code()