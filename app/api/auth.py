from flask import g
from flask_httpauth import HTTPBasicAuth
from app.models import Speaker
from app.api.errors import error_response

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(email, password):
    speaker = Speaker.query.filter_by(email=email).first()
    if speaker is None:
        return False
    g.current_speaker = speaker # TODO: bit nasty
    return speaker.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)
