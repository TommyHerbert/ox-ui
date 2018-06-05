from app import db


class Speaker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<Speaker {}>'.format(self.email)


class Utterance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))
    speaker_id = db.Column(db.Integer, db.ForeignKey('speaker.id'))
    next_id = db.Column(db.Integer, db.ForeignKey('utterance.id'))


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_utterance_id = db.Column(db.Integer, db.ForeignKey('utterance.id'))

