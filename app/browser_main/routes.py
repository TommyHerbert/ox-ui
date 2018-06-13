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

    # TODO: Can this filter be simplified?
    conversation_filter = Conversation.speakers.any(id=current_user.id)

    conversation = Conversation.query.filter(conversation_filter).first()
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
        # TODO: reduce code duplication
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
    conversation = Conversation()

    # TODO: experiment with ways to add multiple speakers at once
    conversation.speakers.append(ox)
    conversation.speakers.append(current_user)

    opener = Utterance(speaker=ox, text='Hello, my name is Ox.')
    conversation.add_utterance(opener)
    form = SaySomethingForm()
    if form.validate_on_submit():
        # TODO: reduce code duplication
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

    # TODO: Does this work?
    conversations = Conversation.query.filter_by(current_user in speakers).all()

    return render_template('all.html',
                           title='all',
                           conversations=conversations)


@bp.route('/about')
@login_required
def about():
    return render_template('about.html', title='about')
