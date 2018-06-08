ox = Speaker(email='project.ox.mail@gmail.com')
thomas = Speaker(email='thomas.aquinas@paris.com')
thomas.set_password('thomas')
buttercup = Speaker(email='buttercup@cattle.com')
buttercup.set_password('buttercup')
for s in [ox, thomas, buttercup]:
    db.session.add(s)
db.session.commit()

thomas = Speaker.query.filter_by(email='thomas.aquinas@paris.com')
conversation = Conversation(speaker=thomas)
db.session.add(conversation)
db.session.commit()

u1 = Utterance()
