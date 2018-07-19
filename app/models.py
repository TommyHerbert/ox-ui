from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta
import base64
import os

speaker_conversation = db.Table('speaker_conversation',
    db.Column('speaker_id', db.Integer, db.ForeignKey('speaker.id')),
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id'))
)


class Speaker(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)

    # all speakers except Ox have passwords
    password_hash = db.Column(db.String(128), nullable=True)

    # API authentication
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiry = db.Column(db.DateTime)

    conversations = db.relationship(
        'Conversation',
        secondary=speaker_conversation,
        backref=db.backref('speakers', lazy='dynamic'),
        lazy='dynamic')
    utterances = \
        db.relationship('Utterance', backref='speaker', lazy='dynamic')

    def __repr__(self):
        return '<Speaker {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def from_dict(self, data, new_speaker=False):
        if 'email' in data:
            self.email = data['email']
        if new_speaker and 'password' in data:
            self.set_password(data['password'])

    def to_dict(self):
        return {'id': self.id, 'email': self.email}

    def get_token(self, seconds_till_expiry=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiry > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiry = now + timedelta(seconds=seconds_till_expiry)
        return self.token

    def revoke_token(self):
        self.token_expiry = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        speaker = Speaker.query.filter_by(token=token).first()
        if speaker is None or speaker.token_expiry < datetime.utcnow():
            return None
        return speaker

    @staticmethod
    def create():
        speaker = Speaker()
        db.session.add(speaker)
        return speaker

    @staticmethod
    def find_by_email(address):
        return Speaker.query.filter_by(email=address).first()


@login.user_loader
def load_speaker(id):
    return Speaker.query.get(int(id))


class Utterance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speaker_id = \
        db.Column(db.Integer, db.ForeignKey('speaker.id'), nullable=False)
    text = db.Column(db.String(128), nullable=False)
    conversation_id = \
        db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        dic = {'id': self.id, 'text': self.text, 'speaker_id': self.speaker_id}
        dic['timestamp'] = self.timestamp.isoformat() + 'Z'
        return dic


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    context = db.Column(db.PickleType())
    utterances = \
        db.relationship('Utterance', backref='conversation', lazy='dynamic')

    def add_speaker(self, speaker):
        self.speakers.append(speaker)

    def add_utterance(self, utterance):
        utterance.conversation = self
        utterance.timestamp = datetime.utcnow()
        self.timestamp = utterance.timestamp

    def get_first_user_utterance(self):
        for u in self.utterances:
            if u.speaker.email != 'project.ox.mail@gmail.com':
                return u
        return None

    def to_dict(self):
        return_dict = {'id': self.id}
        return_dict['timestamp'] = self.timestamp.isoformat() + 'Z'
        return_dict['speakers'] = [s.to_dict() for s in self.speakers]
        return_dict['utterances'] = [u.to_dict() for u in self.utterances]
        return return_dict

    def delete(self):
        for u in self.utterances:
            db.session.delete(u)
        for s in self.speakers:
            self.speakers.remove(s)
        db.session.delete(self)

    @staticmethod
    def create():
        conversation = Conversation()
        conversation.context = []
        db.session.add(conversation)
        return conversation

