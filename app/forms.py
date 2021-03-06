from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import \
    DataRequired, ValidationError, Email, EqualTo, Length
from app.models import Speaker


class SignInForm(FlaskForm):
    email = StringField('email address', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('sign in')


class SignUpForm(FlaskForm):
    email = StringField('email address', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password2_label = 'repeat password'
    password2_validators = [DataRequired(), EqualTo('password')]
    password2 = PasswordField(password2_label, validators=password2_validators)
    submit = SubmitField('sign up')

    def validate_email(self, email):
        speaker = Speaker.query.filter_by(email=email.data).first()
        if speaker is not None:
            raise ValidationError('that email address is already registered')


class SaySomethingForm(FlaskForm):
    text_validators = [DataRequired(), Length(min=1, max=128)]
    text = TextAreaField('text', validators=text_validators)
    send = SubmitField('send')

