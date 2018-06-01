from flask import render_template
from app import app
from app.forms import SignInForm


@app.route('/')
@app.route('/index')
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
    return render_template('index.html', utterances=utterances)


@app.route('/signin')
def sign_in():
    form = SignInForm()
    return render_template('signin.html', title='sign up or sign in', form=form)

