from app import db
from app.api import bp
from app.api.auth import token_auth
from flask import request, jsonify, g
from conversation.mind import Mind
from app.models import Conversation, Utterance


@bp.route('/utterances', methods=['POST'])
@token_auth.login_required
def post_utterance():
    data = request.get_json() or {}
    for field in ['conversation_id', 'speaker_id', 'text']:
        if field not in data:
            return bad_request('missing one or more fields')
    conversation = Conversation.query.get(data['conversation_id'])
    if not conversation:
        return error_response(404, 'no such conversation')
    utterance = Utterance(speaker_id=data['speaker_id'], text=data['text'])
    conversation.add_utterance(utterance)
    Mind().continue_conversation(conversation)
    db.session.commit()
    return jsonify(conversation.to_dict())

