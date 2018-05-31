from app import app


@app.route('/')
@app.route('/index')
def index():
    first_utterance = {'text': 'Hello, my name is Ox.'}
    conversation = {'first_utterance': first_utterance}
    return '''
<html>
    <head>
        <title>Ox</title>
    </head>
    <body>
        <h1>''' + conversation['first_utterance']['text'] + '''</h1>
    </body>
</html>
'''

