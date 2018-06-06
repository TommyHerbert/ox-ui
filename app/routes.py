from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import SignInForm, SaySomethingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Speaker
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    second_utterance = {'text': "Hi Ox, I'm Tommy.", 'next': None}
    first_utterance = {'text': 'Hello, my name is Ox.', 'next': second_utterance}
    conversation = {'first_utterance': first_utterance}
    utterances = []
    utterance = first_utterance
    while True:
        utterances.append(utterance)
        next_utterance = utterance['next']
        if next_utterance:
            utterance = next_utterance
        else:
            break
    form = SaySomethingForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('index.html', utterances=utterances, form=form)


@app.route('/all')
@login_required
def all_my_conversations():
    return render_template('all.html', title='all')


@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = 'sign up or sign in'
    form = SignInForm()
    if form.validate_on_submit():
        speaker = Speaker.query.filter_by(email=form.email.data).first()
        if speaker is None or not speaker.check_password(form.password.data):
            flash('invalid email address or password')
            return redirect(url_for('signin'))
        login_user(speaker)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('signin.html', title=title, form=form)


@app.route('/signout')
def sign_out():
    logout_user()
    return redirect(url_for('sign_in'))


@app.route('/about')
@login_required
def about():
    return render_template('about.html', title='about')
