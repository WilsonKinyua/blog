from flask import render_template, redirect, url_for, flash, request
from . import auth
from flask_login import login_user, logout_user, login_required
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from ..email import send_email


# register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('auth.register'))
        elif User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        elif len(form.password.data) < 8:
            flash('Password must be at least 8 characters', 'danger')
            return redirect(url_for('auth.register'))

        else:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,name=form.name.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully. Please Login', 'success')
            return redirect(url_for('auth.login'))
    title = "Create New Account"
    return render_template('auth/register.html', form=form, title=title)


# login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.profile', username=user.username))
        flash('Invalid username or password', 'danger')
    title = "Login to your account"
    return render_template('auth/login.html', form=form, title=title)


# logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))
