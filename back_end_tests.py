#!/usr/bin/env python
import unittest
from app import create_app, db
from app.models import Speaker, Conversation, Utterance
from config import Config
from conversation.mind import continue_conversation


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class BackEndTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        ox = Speaker(email='project.ox.mail@gmail.com')
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_song(self):
        conversation = Conversation.create()
        user = Speaker(email='user@humans.com')
        question = "What's your favourite song?"
        conversation.utterances.append(Utterance(speaker=user, text=question))
        continue_conversation(conversation)
        self.assertEqual('Hello', conversation.utterances[-1].text)

if __name__ == '__main__':
    unittest.main(verbosity=2)
