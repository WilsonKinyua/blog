from flask import render_template, redirect, url_for, abort, flash, request
from . import main
from flask_login import login_required, current_user
from ..models import User, Role, Post, Comment, Category
from .. import db, photos
from .forms import ProfileForm, CommentForm, CategoryForm
from slugify import slugify
from ..requests import get_quotes


# homepage
@main.route('/')
def index():
    """
        View root page function that returns the index page and its data
    """
    # get all posts
    posts = Post.query.order_by(Post.created_at.desc()).all()
    # get all categories
    categories = Category.query.all()
    # get random quote
    quote = get_quotes()

    return render_template('index.html', posts=posts, categories=categories, quote=quote)


# profile page
@main.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    """
        View profile page function that returns the profile page and its data
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    # update profile form
    form = ProfileForm()
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.name = form.name.data
        user.email = form.email.data
        user.username = form.username.data

    
        # update profile picture
        # if form.profile_pic.data:
        #     filename = photos.save(form.profile_pic.data)
        #     user.profile_pic = photos.url(filename)

        db.session.commit()
        
        flash('You have successfully updated your profile', 'success')

        return redirect(url_for('main.profile', username=user.username))
    form.name.data = user.name
    form.email.data = user.email
    form.username.data = user.username
    form.bio.data = user.bio
    title = 'My Account Profile'

    return render_template("profile/profile.html", user=user, form=form, title=title)
