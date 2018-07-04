from app.api import bp
from app.api.auth import token_auth
from flask import request, jsonify, g


@bp.route('/utterances', methods=['POST'])
@token_auth.login_required
def post_utterance():
    data = request.get_json() or {}
    for field in ['conversation_id', 'speaker_id', 'text']:
        if field not in data:
            return bad_request('missing one or more fields')
    # TODO

