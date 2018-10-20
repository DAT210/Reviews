'''The API portion of the reviews application. Handles API requests.'''

from flask import (
	Flask, g, jsonify, make_response, request, Blueprint
)
from reviews import review
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
def get_review(meal_id):
	rating = review.get(meal_id)
	if rating is None:
		raise APIError(f"The rating for id '{meal_id}' could not be found", status_code=404, type='Not Found')
	elif rating is isinstance(rating, Exception):
		raise APIError(str(rating), status_code=400)
	reply = {
		'status': 'success',
		'data': {
			'review': {
				'id': meal_id,
				'rating': rating,
				'description': f"The id {meal_id} has a rating of {rating} stars."
			}
		}
	}
	return make_response(jsonify(reply)), 200

@bp.route('/reviews/', methods=['GET'])
def get_reviews():
	reviews = review.pull()
	if reviews is None:
		raise APIError("There are no reviews.", status_code=404, type='Not Found')
	reply = {
		'status': 'success',
		'data': { 'reviews': [] }
	}
	replies = reply['data']['reviews']
	for meal_id, rating in reviews:
		replies.append({
			'id': meal_id,
			'rating': rating,
			'description': f"The id {meal_id} has a rating of {rating} stars."
		})
	return make_response(jsonify(reply)), 200

@bp.route('/reviews/', methods=['PATCH'])
def set_review():
	if not request.is_json:
		raise APIError("The request must be in json format.", status_code=400, type='Bad Request')
	if not 'data' in request.get_json():
		raise APIError("The json request is not correctly formatted, \
		missing 'data', see the documentation.", status_code=400, type='Bad Request')
	id_dict = request.get_json()['data']
	(meal_id, rating,) = id_dict.values()
	if not isinstance(meal_review, int):
		raise APIError("The rating must be an integer.", status_code=400, type='Bad Request')
	check, error = review.set(meal_id, rating)
	if check is 0 or None:
		raise APIError("SET_REVIEW")
	reply = {
		'status': 'success',
		'data': None
	}
	return make_response(jsonify(reply)), 200

@bp.route('/reviews/', methods=['POST'])
def add_review():
	if not request.is_json or not 'meal_id' in request.get_json():
		raise APIError("ADD_REVIEW", status_code=400, type='Bad Request')
	check, e = review.add(request.get_json()['meal_id'])
	if check is 0 or None:
		raise APIError(str(e), status_code=409, type='Conflict')
	reply = {
		'status': 'success',
		'data': None
	}
	return make_response(jsonify(reply)), 201

@bp.route('/reviews/<string:meal_id>/', methods=['DELETE'])
def remove_review(meal_id):
	okay = review.remove(meal_id)
	if okay is 0 or None:
		raise APIError("REMOVE_REVIEW", status_code=404, type='Not Found')
	reply = {
		'status': "success",
		'data': None
		}
	return make_response(jsonify(reply)), 200

# Error handling:
@bp.errorhandler(APIError)
def handle_APIError(error):
	reply = {
		'status': 'error',
		'data': error.json()
	}
	return make_response(jsonify(reply))