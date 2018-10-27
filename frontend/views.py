from flask import (
	Flask, g, jsonify, make_response, request, Blueprint, render_template
)
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
            return make_response(jsonify(review_values))
        return "Hello world!"
    else:
        return "Wrong response method"






