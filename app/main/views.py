from flask import render_template, redirect, url_for, abort, flash, request
from . import main
from flask_login import login_required, current_user
from ..models import User, Role, Post, Comment, Category
from .. import db, photos
from .forms import ProfileForm, CommentForm, CategoryForm, PasswordForm
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

        db.session.commit()

        flash('You have successfully updated your profile', 'success')

        return redirect(url_for('main.profile', username=user.username))
    form.name.data = user.name
    form.email.data = user.email
    form.username.data = user.username
    form.bio.data = user.bio

    # update password
    password_form = PasswordForm()
    if password_form.validate_on_submit():
        if current_user.verify_password(password_form.old_password.data):
            current_user.password = password_form.password.data
            db.session.commit()
            flash('You have successfully updated your password', 'success')
            return redirect(url_for('main.profile', username=user.username))
        else:
            flash('Invalid password', 'danger')

    title = 'My Account Profile'

    return render_template("profile/profile.html", user=user, form=form, title=title, password_form=password_form)

# update profile picture


@main.route('/profile/<username>/update/pic', methods=['POST'])
@login_required
def update_pic(username):
    """
        View update profile picture function that returns the update profile picture page and its data
    """
    user = User.query.filter_by(username=username).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
        flash('You have successfully uploaded a profile picture', 'success')
        return redirect(url_for('main.profile', username=username))
    else:
        flash('You have not uploaded a profile picture', 'danger')
        return redirect(url_for('main.profile', username=username))
