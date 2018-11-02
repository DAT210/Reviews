from flask import (
	Flask, g, jsonify, make_response, request, Blueprint, render_template, redirect, url_for, current_app
)
import json
from random import randint
import requests
from frontend.forms import ReviewForm
from jinja2 import TemplateNotFound

bp = Blueprint('api',__name__,url_prefix='/reviews', template_folder='templates')
'''
@bp.route("/history/<string:customer_id>/", methods=['GET'])
def show_history(customer_id):
    previous_orders = None
    if request.method == 'GET':
        response = requests.api.get(f"http://review_api:80/api/1.0/reviews/{meal_id}/", timeout=10.0) #skal være request til orders, trenger en metode som tar inn customer ID og returner alle ordre
        if response.status_code is 200:
            previous_orders = response.json()['data']['previous_orders']    
            return render_template("history.html", previous_orders=previous_orders)
        else:
            return "wrong"
    else:
        return "Wrong response method"
'''

@bp.route("/history/<string:customer_id>/", methods=['GET'])
def show_history(customer_id):
    previous_orders = [{'order_id': i,
        'meals': [randint(0,9) for i in range(0,9)]
        } for i in range(10001, 10006)]
    current_app.logger.info(previous_orders)


    return render_template("history.html", previous_orders=previous_orders)




@bp.route("/form/<string:meal_id>/", methods=['POST', 'GET'])
def show_form(meal_id):
    form = ReviewForm()
    review = None
    if request.method == 'GET':
        response = requests.api.get(f"http://review_api:80/api/1.0/reviews/{meal_id}/", timeout=10.0)
        if response.status_code is 200: 
            review = response.json()['data']['review']
            return render_template("review.html", form = form, review=review)
        else:
            return "wrong"
 #       if response.status_code is 400:

    #      if response.status_code is 404:
    elif request.method == 'POST':
        if form.validate_on_submit:
            review_values = request.form.to_dict()
            try:
                ratingInt = int(review_values.pop('rating'))
            except ValueError:
                return "Value error"
            response = {
                'data': {
                    'id': meal_id,
                    'rating': ratingInt,
                    'comment': review_values.pop('comments')
                }
            }
            api_response = requests.api.patch("http://review_api:80/api/1.0/reviews/", json=response)
            if len(form.comments.data) > 255:
                return render_template("review.html", form = form, review=review)

            try:
                status = api_response.json().get('status')
            except json.decoder.JSONDecodeError as err:
                return render_template("review.html", status=err)
            
            if status == 'success':
                return redirect(url_for("api.show_history", customer_id="1")) #skal være history/x, hvor x er riktig customer_id

                
        return render_template("review.html", form=form)
 
    else:
        return "Wrong response method"





 
