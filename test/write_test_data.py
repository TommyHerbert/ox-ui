for u in Utterance.query.all():
    db.session.delete(u)
for c in Conversation.query.all():
    db.session.delete(c)
for s in Speaker.query.all():
    db.session.delete(s)
db.session.commit()


ox = Speaker(email='project.ox.mail@gmail.com')
thomas = Speaker(email='thomas.aquinas@paris.com')
thomas.set_password('thomas')
buttercup = Speaker(email='buttercup@cattle.com')
buttercup.set_password('buttercup')
for s in [ox, thomas, buttercup]:
    db.session.add(s)
db.session.commit()

thomas = Speaker.query.filter_by(email='thomas.aquinas@paris.com').first()
conversation = Conversation(speaker=thomas)
db.session.add(conversation)
db.session.commit()

ox = Speaker.query.filter_by(email='project.ox.mail@gmail.com').first()
conversation = Conversation.query.all()[0]
u1 = Utterance(speaker=ox,
               text='Hello, my name is Ox.',
               conversation=conversation,
               order_number=1)
u2 = Utterance(speaker=thomas,
               text="What's your favourite Adele song?",
               conversation=conversation,
               order_number=2)
u3 = Utterance(speaker=ox,
               text="Hello.",
               conversation=conversation,
               order_number=3)
for u in [u1, u2, u3]:
    db.session.add(u)
db.session.commit()
