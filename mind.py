from app import create_app
app = create_app()
app.app_context().push()
from app.models import Speaker, Utterance

ox = Speaker.query.filter_by(email='project.ox.mail@gmail.com').first()


def start_conversation():
    pass # TODO


def continue_conversation(conversation):
    utterance = Utterance(speaker=ox, text='Hello.')
    conversation.add_utterance(utterance)

