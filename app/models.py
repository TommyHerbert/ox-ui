from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Speaker(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)

    # All speakers except Ox have passwords.
    password_hash = db.Column(db.String(128), nullable=True)

    conversations = \
        db.relationship('Conversation', backref='speaker', lazy='dynamic')

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
    order_number = db.Column(db.Integer, nullable=False)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speaker_id = \
        db.Column(db.Integer, db.ForeignKey('speaker.id'), nullable=False)
    utterances = \
        db.relationship('Utterance', backref='conversation', lazy='dynamic')

