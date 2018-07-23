#!/usr/bin/env python
import unittest
from app import create_app, db
from app.models import Speaker, Conversation, Utterance
from config import Config
from conversation.mind import continue_conversation


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    '''
    TODO: This isn't working as it should. Maybe it's not happening at
    all; maybe it's happening and then something else is over-riding
    it; maybe come parts of the code are using the test config and
    others are using the app config.
    '''


class BackEndTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.test_user = Speaker(email='user@test.com')
        db.session.add(self.test_user)
        db.session.commit()
    
    def tearDown(self):
        for u in Utterance.query.filter_by(speaker=self.test_user):
            db.session.delete(u)
        conversation_filter = Conversation.speakers.any(id=self.test_user.id)
        for c in Conversation.query.filter(conversation_filter).all():
            db.session.delete(c)
        db.session.delete(self.test_user)
        db.session.commit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_song(self):
        conversation = Conversation.create()
        db.session.add(conversation)
        db.session.commit()
        
        question = "What's your favourite song?"
        utterance = Utterance(speaker=self.test_user, text=question, conversation=conversation)
        db.session.add(utterance)
        db.session.commit()
        continue_conversation(conversation)
        self.assertEqual('Hello', conversation.utterances[-1].text)
        db.session.delete(conversation)
        db.session.delete(utterance)
        db.session.commit()

    def test_nothing_much(self):
        self.assertEqual(1, 1)

#    def test_adele_song(self):
#        conversation = Conversation.create()
#        user = Speaker(email='user2@humans.com')
#        question = "What's your favourite Adele song?"
#        conversation.utterances.append(Utterance(speaker=user, text=question))
#        continue_conversation(conversation)
#        self.assertEqual('Hello', conversation.utterances[-1].text)
#
#    def test_dont_understand(self):
#        self._assert_response('Hello Ox.', "Sorry, I didn't understand that.")
#        
#    def _assert_response(self, utterance, response):
#        conversation = Conversation.create()
#        user = Speaker(email='user@humans.com')
#        conversation.utterances.append(Utterance(speaker=user, text=utterance))
#        continue_conversation(conversation)
#        self.assertEqual(response, conversation.utterances[-1].text)

    # TODO: adapt the other back end tests from the ox project


if __name__ == '__main__':
    unittest.main(verbosity=2)

