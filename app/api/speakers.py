from app import db
from app.api import bp
from app.api.auth import token_auth
from app.models import Speaker
from flask import request, jsonify


@bp.route('/speakers', methods=['POST'])
def create_speaker():
    data = request.get_json() or {}
    if 'email' not in data or 'password' not in data:
        return bad_request('must include email and password fields')
    if Speaker.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    speaker = Speaker.create()
    speaker.from_dict(data, new_speaker=True)
    db.session.commit()
    response = jsonify({'id': speaker.id})
    response.status_code = 201
    return response


@bp.route('/speakers/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_speaker(id):
    pass # TODO


@bp.route('/speakers/<int:id>/conversations', methods=['GET'])
@token_auth.login_required
def get_conversations_for_speaker(id):
    pass # TODO


@bp.route('/speakers/<int:id>/conversations/latest', methods=['GET'])
@token_auth.login_required
def get_latest_conversation_for_speaker(id):
    pass # TODO

