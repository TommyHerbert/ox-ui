from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import Speaker
from app.api.errors import error_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(email, password):
    speaker = Speaker.query.filter_by(email=email).first()
    if speaker is None:
        return False
    g.current_speaker = speaker
    return speaker.check_password(password)


@token_auth.verify_token
def verify_token(token):
    g.current_speaker = Speaker.check_token(token) if token else None
    return g.current_speaker is not None


@basic_auth.error_handler
@token_auth.error_handler
def token_auth_error():
    return error_response(401)

