from flask_wtf import FlaskForm, csrf 
from wtforms import RadioField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ReviewForm(FlaskForm):
    rating_stars = "<i class='fa fa-star-o'></i><i class='fa fa-star'></i>"
    rating = RadioField('rating', validators=[DataRequired()], choices = [(5, rating_stars), (4, rating_stars), (3, rating_stars), (2, rating_stars), (1, rating_stars) ])
    comments = TextAreaField('Comments: ', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('submit')
