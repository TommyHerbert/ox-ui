from app import create_app
app = create_app()
app.app_context().push()
from app.models import Speaker, Utterance
from knowledge.knowledge_base import KnowledgeBase
from conversation.reader import Reader
from conversation.strategy import NaiveConversationStrategy
from conversation.reasoner import Reasoner
from conversation.speaker import Speaker

ox = Speaker.query.filter_by(email='project.ox.mail@gmail.com').first()
knowledge_base = KnowledgeBase()
reader = Reader(knowledge_base)
strategy = NaiveConversationStrategy()
reasoner = Reasoner()
speaker = Speaker()


def start_conversation(conversation):
    conversation.speakers.append(ox)
    utterance = Utterance(speaker=ox, text='Hello, my name is Ox.')
    conversation.add_utterance(utterance)


def continue_conversation(conversation):
    reader.read_last_move(conversation)
    next_move = strategy.pop_move(conversation.context)
    answer_concept = reasoner.take_move(next_move)
    utterance = Utterance(speaker=ox, text=speaker.utter(answer_concept))
    conversation.add_utterance(utterance)

