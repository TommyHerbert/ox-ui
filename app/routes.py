from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    first_utterance = {'text': 'Hello, my name is Ox.'}
    conversation = {'first_utterance': first_utterance}
    return render_template('index.html', conversation=conversation)

