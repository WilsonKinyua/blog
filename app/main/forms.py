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
    # password = PasswordField('Password', validators=[Required(), Length(6, 64), EqualTo('password2', message='Passwords must match')])
    # password2 = PasswordField('Confirm Password', validators=[Required()])
    bio = TextAreaField('About Me')
    submit = SubmitField('Update Profile')