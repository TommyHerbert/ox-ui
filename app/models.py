from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

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


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    utterances = \
        db.relationship('Utterance', backref='conversation', lazy='dynamic')

    def add_utterance(self, utterance):
        utterance.conversation = self
        utterance.timestamp = datetime.utcnow()
        self.timestamp = utterance.timestamp
        db.session.add(utterance)

    def get_first_user_utterance(self):
        for u in self.utterances:
            if u.speaker.email != 'project.ox.mail@gmail.com':
                return u
        return None

