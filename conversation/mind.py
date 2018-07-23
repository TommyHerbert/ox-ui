from app.models import Speaker, Utterance
from knowledge.knowledge_base import KnowledgeBase
from conversation.reader import Reader
from conversation.strategy import NaiveConversationStrategy
from conversation.reasoner import Reasoner
from conversation.expresser import Expresser

class Mind:
    def __init__(self):
        self.ox = Speaker.find_by_email('project.ox.mail@gmail.com')
        self.knowledge_base = KnowledgeBase()
        self.reader = Reader(self.knowledge_base)
        self.strategy = NaiveConversationStrategy()
        self.reasoner = Reasoner()
        self.expresser = Expresser()

    def start_conversation(self, conversation):
        conversation.speakers.append(self.ox)
        utterance = Utterance(speaker=self.ox, text='Hello, my name is Ox.')
        conversation.add_utterance(utterance)

    def continue_conversation(self, conversation):
        self.reader.read_last_move(conversation)
        next_move = self.strategy.pop_move(conversation.context)
        answer_concept = self.reasoner.take_move(next_move)
        text = self.expresser.express(answer_concept)
        conversation.add_utterance(Utterance(speaker=self.ox, text=text))

