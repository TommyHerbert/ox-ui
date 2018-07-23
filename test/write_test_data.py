from app.models import Utterance, Conversation, Speaker
from app import db
from datetime import datetime, timedelta

for u in Utterance.query.all():
    db.session.delete(u)
for c in Conversation.query.all():
    db.session.delete(c)
for s in Speaker.query.all():
    db.session.delete(s)
db.session.commit()

ox = Speaker(email='project.ox.mail@gmail.com')
thomas = Speaker(email='thomas.aquinas@paris.com')
thomas.set_password('aquinas')
buttercup = Speaker(email='buttercup@cattle.com')
buttercup.set_password('buttercup')
for s in [ox, thomas, buttercup]:
    db.session.add(s)

conversation_start = datetime.utcnow() - timedelta(seconds=2)
conversation = Conversation(timestamp=conversation_start)
conversation.speakers.append(ox)
conversation.speakers.append(thomas)
conversation.context = []
db.session.add(conversation)

u1 = Utterance(speaker=ox,
               text='Hello, my name is Ox.',
               conversation=conversation,
               timestamp=conversation_start)
u2 = Utterance(speaker=thomas,
               text="What's your favourite Adele song?",
               conversation=conversation,
               timestamp=conversation_start + timedelta(seconds=1))
u3 = Utterance(speaker=ox,
               text="Hello.",
               conversation=conversation,
               timestamp=conversation_start + timedelta(seconds=2))
for u in [u1, u2, u3]:
    db.session.add(u)
db.session.commit()
