from flask import render_template, flash, redirect
from app import app
from app.forms import SignInForm, SaySomethingForm


@app.route('/')
def root_route():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
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
        return redirect('/index')
    return render_template('index.html', utterances=utterances, form=form)


@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    title = 'sign up or sign in'
    form = SignInForm()
    if form.validate_on_submit():
        flash('Sign up or sign in requested for {}'.format(form.email.data))
    return render_template('signin.html', title=title, form=form)

