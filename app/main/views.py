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
    # get current user posts
    user = User.query.filter_by(username=username).first()
    posts = Post.get_user_posts(
        user.id).order_by(Post.created_at.desc()).all()
    if user is None:
        abort(404)
    # get all categories
    categories = Category.query.all()
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

    return render_template("profile/profile.html",
                           user=user,
                           form=form,
                           title=title,
                           password_form=password_form,
                           categories=categories,
                           posts=posts
                           )

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

# create a new post


@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """
        View new post function that returns the new post page and its data
    """
    title = request.args.get('title')
    category_id = request.args.get('category_id')
    content = request.args.get('content')
    user_id = request.args.get('user_id')

    # filename = photos.save(request.files['photo'])
    # path = f'photos/{filename}'

    post = Post(
        title=title,
        content=content,
        category_id=category_id,
        user_id=user_id,
        # image_path=path
    )

    db.session.add(post)
    db.session.commit()
    # if photo request is not empty then save the photo to the database and update the post image path to the photo path
    # if request.files['photo']:
    #     filename = photos.save(request.files['photo'])
    #     path = f'photos/{filename}'
    #     post.image_path = path
    #     db.session.commit()

    flash('You have successfully created a new post. Proceed and upload the post photo image to display on homepage', 'success')

    return redirect(url_for('main.profile', username=current_user.username))


# update post
@main.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_post(id):
    """
        View update post function that returns the update post page and its data
    """
    post = Post.get_post(id)
    # if post.user_id != current_user:
    #     abort(403)
    title = request.args.get('title')
    category_id = request.args.get('category_id')
    content = request.args.get('content')
    user_id = request.args.get('user_id')
    # update post
    post.title = title
    post.content = content
    post.category_id = category_id
    post.user_id = user_id
    db.session.commit()
    return redirect(url_for('main.profile', username=current_user.username))

# delete post


@main.route('/post/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    """
        View delete post function that returns the delete post page and its data
    """
    post = Post.get_post(id)
    # if post.user_id != current_user:
    #     abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('You have successfully deleted the post', 'success')
    return redirect(url_for('main.profile', username=current_user.username))
