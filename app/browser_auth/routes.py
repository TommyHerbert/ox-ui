from flask import render_template, flash, redirect, url_for, request
from app import db
from app.browser_auth.forms import SignInForm, SignUpForm
from flask_login import current_user, login_user, logout_user
from app.models import Speaker
from werkzeug.urls import url_parse
from app.browser_auth import bp


@bp.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('browser_main.index'))
    form = SignInForm()
    if form.validate_on_submit():
        speaker = Speaker.query.filter_by(email=form.email.data).first()
        if speaker is None or not speaker.check_password(form.password.data):
            flash('invalid email address or password')
            return redirect(url_for('browser_auth.sign_in'))
        login_user(speaker)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('browser_main.index')
        return redirect(next_page)
    return render_template('auth/signin.html', title='sign in', form=form)


@bp.route('/signout')
def sign_out():
    logout_user()
    return redirect(url_for('browser_auth.sign_in'))


@bp.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('browser_main.index'))
    form = SignUpForm()
    if form.validate_on_submit():
        speaker = Speaker.creat()
        speaker.email = form.email.data
        speaker.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('browser_auth.sign_in'))
    return render_template('auth/signup.html', title='sign up', form=form)

