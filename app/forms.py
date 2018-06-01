from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class SignInForm(FlaskForm):
    email = StringField('email address', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    sign_up = SubmitField('sign up')
    sign_in = SubmitField('sign in')


class SaySomethingForm(FlaskForm):
    text = StringField('text', validators=[DataRequired()])
    send = SubmitField('send')

