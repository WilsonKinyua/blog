from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
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
