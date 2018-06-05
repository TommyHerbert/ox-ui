from app import app
from app.models import Speaker, Utterance, Conversation


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Speaker': Speaker,
        'Utterance': Utterance,
        'Conversation': conversation
    }

