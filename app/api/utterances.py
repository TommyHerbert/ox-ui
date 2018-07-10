from app.api import bp
from app.api.auth import token_auth
from flask import request, jsonify, g
from conversation import mind


@bp.route('/utterances', methods=['POST'])
@token_auth.login_required
def post_utterance():
    data = request.get_json() or {}
    for field in ['conversation_id', 'speaker_id', 'text']:
        if field not in data:
            return bad_request('missing one or more fields')
    conversation = Conversation.query.get(id)
    if not conversation:
        return error_response(404, 'no such conversation')
    utterance = Utterance(speaker_id=data['speaker_id'], text=data['text'])
    conversation.add_utterance(utterance)
    mind.continue_conversation(conversation)
    db.session.commit()

