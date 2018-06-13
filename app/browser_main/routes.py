from flask import render_template, flash, redirect, url_for, request
from app import db
from app.browser_main.forms import SaySomethingForm
from flask_login import current_user, login_required
from app.models import Speaker, Utterance, Conversation
from app.browser_main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    query = Conversation.query.filter_by(speaker=current_user) \
                              .order_by(Conversation.timestamp.desc())
    conversation = query.first()
    if not conversation:
        return redirect(url_for('browser_main.new'))
    return redirect(url_for('browser_main.conversation', id=conversation.id))


@bp.route('/conversations/<id>', methods=['GET', 'POST'])
@login_required
def conversation(id):
    conversation = Conversation.query.get(id)
    if not conversation:
        return 'no such conversation', 404
    if conversation.speaker != current_user:
        return "tried to view another user's conversation", 403
    utterances = conversation.utterances
    form = SaySomethingForm()
    if form.validate_on_submit():
        utterance = Utterance(speaker=current_user, text=form.text.data)
        conversation.add_utterance(utterance)
        ox = Speaker.query.filter_by(email='project.ox.mail@gmail.com').first()
        reply = Utterance(speaker=ox, text='Hello.')
        conversation.add_utterance(reply)
        db.session.commit()
        return redirect(url_for('browser_main.conversation', id=conversation.id))
    return render_template('index.html', utterances=utterances, form=form)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    ox = Speaker.query.filter_by(email='project.ox.mail@gmail.com').first()
    conversation = Conversation(speaker=current_user)
    opener = Utterance(speaker=ox, text='Hello, my name is Ox.')
    conversation.add_utterance(opener)
    form = SaySomethingForm()
    if form.validate_on_submit():
        utterance = Utterance(speaker=current_user, text=form.text.data)
        conversation.add_utterance(utterance)
        reply = Utterance(speaker=ox, text='Hello.')
        conversation.add_utterance(reply)
        db.session.commit()
        return redirect(url_for('browser_main.index'))
    db.session.commit()
    return render_template('index.html', utterances=[opener], form=form)


@bp.route('/all')
@login_required
def all_my_conversations():
    conversations = Conversation.query.filter_by(speaker=current_user).all()
    return render_template('all.html',
                           title='all',
                           conversations=conversations)


@bp.route('/about')
@login_required
def about():
    return render_template('about.html', title='about')
