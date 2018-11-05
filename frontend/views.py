'''The standard views of the review part of the application.'''

from flask import (
		Flask, g, jsonify, make_response, request, Blueprint, render_template,
	session, url_for, redirect, flash, current_app
)
import requests
import json
from random import randint
from frontend.forms import ReviewForm

bp = Blueprint('reviews',__name__,url_prefix='/reviews', template_folder='templates')


@bp.route("/history/<string:customer_id>/", methods=['GET'])
def show_history(customer_id):
    previous_orders = [{'order_id': i,
        'meals': [randint(0,9) for i in range(0,9)]
        } for i in range(10001, 10006)]
    current_app.logger.info(previous_orders)


    return render_template("history.html", previous_orders=previous_orders)

@bp.route('/hello/', methods=['GET', 'POST'])
def reviews():
	return "Hello, Reviews!"

@bp.route("/<string:meal_id>/", methods=['POST', 'GET'])
def show_form(meal_id):
	form = ReviewForm()
	if request.method == 'POST':
		if form.validate_on_submit:
			review_values = request.form.to_dict()
			try:
				ratingInt = int(review_values.pop('rating', 'None'))
			except ValueError:
				flash('The rating must be set.', category='warning')
				return redirect(url_for('reviews.show_form', meal_id=meal_id))
			comment_len = len(form.comments.data)
			if 4 > comment_len or comment_len > 255:
				# Set the flash category as a bootstrap alert class to colour it.
				flash("The comment must be between 4 and 255 characters.", category='warning')
				return redirect(url_for('reviews.show_form', meal_id=meal_id))
			payload = {
				'data': {
					'id': meal_id,
					'rating': ratingInt,
					'comment': review_values.pop('comments')
				}
			}
			try:
				api_response = requests.api.patch("http://review_api:80/api/1.0/reviews/", json=payload, timeout=30.0)
			except:
				flash("The server couldn't reach the API.", category='info')
				return redirect(url_for('reviews.show_form', meal_id=meal_id))
			try:
				status = api_response.json().get('status')
			except json.decoder.JSONDecodeError as err:
				return render_template("dummy.html", status=err)
			if status == 'success':
				flash('The review has successfully been added!', category='success')
				return redirect(url_for("reviews.show_history", customer_id="1"))
		flash("The form couldn't be validated.", category='warning')	
		return redirect(url_for('reviews.show_form', meal_id=meal_id))
	try:
		response = requests.api.get(f"http://review_api:80/api/1.0/reviews/{meal_id}/", timeout=30.0)
	except:
		flash("The server couldn't reach the API.", category='info')
		return redirect(url_for('reviews.show_form', meal_id=meal_id)), 500
	if response.status_code is 200:
		review = response.json()['data']['review']
		return render_template("review.html", form=form, review=review)
	else:
		return redirect(url_for('reviews.show_form', meal_id=meal_id))

