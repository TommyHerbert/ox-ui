from app.api import bp
from app.models import Conversation
from flask import jsonify
from app import db
from app.api.auth import token_auth


@bp.route('/conversations', methods=['POST'])
@token_auth.login_required
def create_conversation(data):
    pass # TODO


@bp.route('/conversations/<int:id>', methods=['GET'])
@token_auth.login_required
def get_conversation(id):
    # TODO: current speaker should be one of the participants
    return jsonify(Conversation.query.get_or_404(id).to_dict())


@bp.route('/conversations/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_conversation(id):
    # TODO: current speaker should be one of the participants
    conversation = Conversation.query.get_or_404(id)
    conversation.delete()
    db.session.commit()
    return '', 204

