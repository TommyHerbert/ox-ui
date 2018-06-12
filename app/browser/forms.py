from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class SaySomethingForm(FlaskForm):
    text_validators = [DataRequired(), Length(min=1, max=128)]
    text = TextAreaField('text', validators=text_validators)
    send = SubmitField('send')

