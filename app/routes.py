from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import SignInForm, SignUpForm, SaySomethingForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Speaker, Utterance
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    query = Utterance.query.filter_by(speaker=current_user) \
                           .order_by(Utterance.timestamp.desc())
    conversation = query.first().conversation
    utterances = conversation.utterances
    form = SaySomethingForm()
    if form.validate_on_submit():
        utterance = Utterance(speaker=current_user,
                              text=form.text.data,
                              conversation=conversation)
        db.session.add(utterance)
        db.session.commit()
        ox = Speaker.query.filter_by(email='project.ox.mail@gmail.com').first()
        reply = Utterance(speaker=ox, text='Hello.', conversation=conversation)
        db.session.add(reply)
        db.session.commit()
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
    form = SignInForm()
    if form.validate_on_submit():
        speaker = Speaker.query.filter_by(email=form.email.data).first()
        if speaker is None or not speaker.check_password(form.password.data):
            flash('invalid email address or password')
            return redirect(url_for('sign_in'))
        login_user(speaker)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('signin.html', title='sign in', form=form)


@app.route('/signout')
def sign_out():
    logout_user()
    return redirect(url_for('sign_in'))


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        speaker = Speaker(email=form.email.data)
        speaker.set_password(form.password.data)
        db.session.add(speaker)
        db.session.commit()
        return redirect(url_for('sign_in'))
    return render_template('signup.html', title='sign up', form=form)


@app.route('/about')
@login_required
def about():
    return render_template('about.html', title='about')
