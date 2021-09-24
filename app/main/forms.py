from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import Post, Comment, Subscriber
from wtforms import ValidationError


# comment form
class CommentForm(FlaskForm):
    body = StringField('Comment', validators=[Required()])
    submit = SubmitField('Submit')


# subscriber form
class SubscriberForm(FlaskForm):
    email = StringField('Email', validators=[
                        Required(), Length(1, 64), Email()])
    submit = SubmitField('Subscribe')


# category form
class CategoryForm(FlaskForm):
    name = StringField('Category', validators=[Required()])
    submit = SubmitField('Submit')


# profile form
class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    username = StringField('Username', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    bio = TextAreaField('About Me')
    submit = SubmitField('Update Profile')

# password change form


class PasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[Required()])
    password = PasswordField('New Password', validators=[
                             Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Update Password')
