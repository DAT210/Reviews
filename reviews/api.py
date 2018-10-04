from flask import (
	Flask, g, jsonify, make_response, request, abort, Blueprint
)
from . import review, db

bp = Blueprint('api',__name__,url_prefix='')

@bp.route('/todo/api/v1.0/review/get/<string:meal_id>', methods=['GET'])
def get_review(meal_id):
	r = review.get(meal_id)
	x = {
		'id': meal_id,
		'review': r,
		'description': f"ID: {meal_id} has the review {r}"
	}
	return jsonify(x)

@bp.route('/', methods=['GET'])
def get_reviews():
   return jsonify({'reviews': reviews})

@bp.route('/todo/api/v1.0/review/set/<string:meal_id>/<int:re>', methods=['GET'])
def set_review(meal_id, re):
	#if not request.json or not 'meal_id' in request.json:
		#abort(400)
	review.set(meal_id, re)
	return jsonify({'ok': 'success'})

@bp.route('/todo/api/v1.0/review/add/<string:meal_id>', methods=['GET'])
def add_review(meal_id):
	review.add(meal_id)
	return jsonify({'ok': 'success'})

@bp.route('/todo/api/v1.0/review/remove/<string:meal_id>', methods=['GET'])
def remove_review(meal_id):
	review.remove(meal_id)
	return jsonify({'ok': 'success'})

# Error handling:
@bp.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': "Not found"}), 404)