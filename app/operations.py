from app import db
from app.models import Conversation
from conversation.mind import Mind


def create_conversation(speaker):
    conversation = Conversation.create()
    conversation.add_speaker(speaker)
    Mind().start_conversation(conversation)
    db.session.commit()
    return conversation

