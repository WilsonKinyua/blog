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
            flash('Email already exists')
            return redirect(url_for('auth.register'))
        elif User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        elif len(form.password.data) < 8:
            flash('Password must be at least 8 characters')
            return redirect(url_for('auth.register'))

        else:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully. Please Login')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
