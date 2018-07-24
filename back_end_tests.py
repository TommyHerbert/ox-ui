#!/usr/bin/env python
import unittest
from app import create_app, db
from app.models import Speaker, Conversation, Utterance
from config import Config
from conversation.mind import Mind
from knowledge.myself import Myself


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class BackEndTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.ox = Speaker(email='project.ox.mail@gmail.com')
        self.test_user = Speaker(email='test@users.com')
        for s in [self.ox, self.test_user]:
            db.session.add(s)
        db.session.commit()

        self.conversation = Conversation.create()
        for s in [self.ox, self.test_user]:
            self.conversation.speakers.append(s)
        db.session.add(self.conversation)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_goal(self):
        self.assertEqual('do good by teaching', Myself().goal)

    def test_song(self):
        self._assert_response("What's your favourite song?", 'Hello')

    def test_adele_song(self):
        self._assert_response("What's your favourite Adele song?", 'Hello')

    def test_dont_understand(self):
        self._assert_response('Hello Ox.', "Sorry, I didn't understand that.")

    def test_favourite_foo(self):
        test_input = "What's your favourite foo?"
        expected_response = "Sorry, I didn't understand that."
        self._assert_response(test_input, expected_response)

    def test_favourite_foo_song(self):
        test_input = "What's your favourite foo song?"
        expected_response = "Sorry, I didn't understand that."
        self._assert_response(test_input, expected_response)

    def test_favourite_adele_foo(self):
        test_input = "What's your favourite Adele foo?"
        expected_response = "Sorry, I didn't understand that."
        self._assert_response(test_input, expected_response)

    def test_(self):
        test_input = ""
        expected_response = "Sorry, I didn't understand that."
        self._assert_response(test_input, expected_response)

    def _assert_response(self, test_input, response):
        utterance = Utterance(speaker=self.test_user,
                              text=test_input,
                              conversation=self.conversation)
        db.session.add(utterance)
        db.session.commit()

        Mind().continue_conversation(self.conversation)
        self.assertEqual(response, self.conversation.utterances[-1].text)


if __name__ == '__main__':
    unittest.main(verbosity=2)

