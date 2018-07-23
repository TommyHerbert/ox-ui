from flask import render_template, flash, redirect, url_for, request
from app import db
from app.browser_main.forms import SaySomethingForm
from flask_login import current_user, login_required
from app.models import Speaker, Utterance, Conversation
from app.browser_main import bp
from conversation.mind import Mind
from app.operations import create_conversation


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    conversation_filter = Conversation.speakers.any(id=current_user.id)
    conversation = Conversation.query.filter(conversation_filter) \
                                     .order_by(Conversation.timestamp.desc()) \
                                     .first()
    if not conversation:
        return redirect(url_for('browser_main.new'))
    return redirect(url_for('browser_main.conversation', id=conversation.id))


@bp.route('/conversations/<id>', methods=['GET', 'POST'])
@login_required
def conversation(id):
    conversation = Conversation.query.get(id)
    if not conversation:
        return 'no such conversation', 404
    if current_user not in conversation.speakers:
        return "tried to view another user's conversation", 403
    return _set_up_say_something_form(conversation)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    conversation = create_conversation(current_user)
    return _set_up_say_something_form(conversation, new=True)


@bp.route('/all')
@login_required
def all_my_conversations():
    conversation_filter = Conversation.speakers.any(id=current_user.id)
    conversations = Conversation.query.filter(conversation_filter).all()
    return render_template('all.html',
                           title='all',
                           conversations=conversations)


@bp.route('/about')
@login_required
def about():
    return render_template('about.html', title='about')


def _set_up_say_something_form(conversation, new=False):
    utterances = conversation.utterances
    form = SaySomethingForm()
    if form.validate_on_submit():
        utterance = Utterance(speaker=current_user, text=form.text.data)
        conversation.add_utterance(utterance)
        Mind().continue_conversation(conversation)
        db.session.commit()
        if new:
            return redirect(url_for('browser_main.index'))
        else:
            return redirect(url_for('browser_main.conversation', id=conversation.id))
    return render_template('index.html', utterances=utterances, form=form)
