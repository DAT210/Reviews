from flask import (
	Flask, g, jsonify, make_response, request, Blueprint, render_template, redirect
)
import json
import requests
from frontend.forms import ReviewForm
from jinja2 import TemplateNotFound

bp = Blueprint('api',__name__,url_prefix='/form', template_folder='templates')

@bp.route("/<string:meal_id>/", methods=['POST', 'GET'])
def show_form(meal_id):
    form = ReviewForm()
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
                return "Don't fuck with the html"

            try:
                status = api_response.json().get('status')
            except json.decoder.JSONDecodeError as err:
                return render_template("dummy.html", status=err)
            
            if status == 'success':
                return render_template("dummy.html", status=status) #skal være Redirect til order history

                
        return render_template("review.html", form=form)
 
    else:
        return "Wrong response method"






