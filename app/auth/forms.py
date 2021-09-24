from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import User
from wtforms import ValidationError


class LoginForm(FlaskForm):
    """
        Login form
    """
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """
        Registration form
    """
    name = StringField('Full Name', validators=[Required()])
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    email = StringField('Email', validators=[
                        Required(), Email(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required(), EqualTo(
        'password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Create Account')

    def validate_check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(
                'Email already registered. Please proceed to login!')

    def validate_check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                'Username already in use. Please use another username.')
