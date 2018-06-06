from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Speaker(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

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
    text = db.Column(db.String(128))
    speaker_id = db.Column(db.Integer, db.ForeignKey('speaker.id'))
    next_id = db.Column(db.Integer, db.ForeignKey('utterance.id'))


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speaker.id'))
    first_utterance_id = db.Column(db.Integer, db.ForeignKey('utterance.id'))

