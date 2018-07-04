from app import db
from app.models import Conversation
import mind


def create_conversation(speaker):
    conversation = Conversation.create()
    conversation.add_speaker(speaker)
    mind.start_conversation(conversation)
    db.session.commit()
    return conversation

