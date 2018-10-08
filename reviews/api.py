from flask import (
	Flask, g, jsonify, make_response, request, abort, Blueprint
)
import review, db

bp = Blueprint('api',__name__,url_prefix='/api/1.0')

@bp.route('/test', methods=['GET'])
def test():
	dbb = db.get_db()
	print(f"TEST: {dbb}")
	return jsonify({'test': "Success!"})

@bp.route('/reviews/<string:meal_id>', methods=['GET'])
def get_review(meal_id):
	r = review.get(meal_id)
	if r is None:
		abort(400)
	x = {
		'id': meal_id,
		'review': r,
		'description': f"ID: {meal_id} has the review {r}"
	}
	return jsonify(x)

@bp.route('/reviews', methods=['GET'])
def get_reviews():
   return jsonify({'reviews': 'N/A'})

@bp.route('/reviews/', methods=['PATCH'])
def set_review():
	if not request.json or not 'meal_id' in request.json:
		abort(400)
	review.set(meal_id, re)
	return jsonify({'ok': 'success'})

@bp.route('/reviews', methods=['POST'])
def add_review():
	review.add(meal_id)
	return jsonify({'ok': 'success'})

@bp.route('/reviews/<string:meal_id>', methods=['DELETE'])
def remove_review(meal_id):
	review.remove(meal_id)
	return jsonify({'ok': 'success'})

# Error handling:
@bp.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': {
		'code': 404,
		'message': "Some message.",
		'type': "The type of error."
	}}), 404)

@bp.errorhandler(400)
def none_type(error):
	return make_response(jsonify({
		'error': {
			'code': 400,
			'message': "The specified id does not exist.",
			'type': "MEH"
		}
	}))