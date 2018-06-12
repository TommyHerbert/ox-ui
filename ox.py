from app import create_app, db
from app.models import Speaker, Utterance, Conversation

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Speaker': Speaker,
        'Utterance': Utterance,
        'Conversation': Conversation
    }

