from app.api import bp
from app.api.auth import token_auth

@bp.route('/utterances', methods=['POST'])
@token_auth.login_required
def post_utterance(data):
    pass # TODO

