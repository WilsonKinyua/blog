from flask import render_template, redirect, url_for, abort, flash, request
from . import main
from flask_login import login_required, current_user
from ..models import Subscriber, User, Role, Post, Comment, Category
from .. import db, photos
from .forms import ProfileForm, CommentForm, CategoryForm, PasswordForm
from slugify import slugify
from ..requests import get_quotes
from ..email import send_email
# import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url


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
    # get latest 5 posts
    latest_posts = Post.query.order_by(Post.created_at.desc()).limit(4)

    return render_template('index.html', posts=posts, categories=categories, quote=quote, latest_posts=latest_posts)

# single post


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def single_post(id):
    """
        View post page function that returns the post details page and its data
    """
    # get post by id
    post = Post.get_post(id)
    # add comment form
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            post_id=post.id,
            post_owner_id=post.user_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('.single_post', id=post.id))
    # get all comments
    comments = Comment.get_comments_by_post(post.id)
    return render_template('single_post.html', post=post, form=form, comments=comments)


# filter posts by category
@main.route('/category/<int:id>')
def filter_posts(id):
    """
        View posts page function that returns the posts filtered by category
    """
    # get category by id
    category = Category.query.filter_by(id=id).first()
    # get all posts by category
    posts = Post.get_post_by_category(category.id)
    return render_template('posts.html', posts=posts, category=category)

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
    # get all comments created by other users on current user posts
    comments = Comment.get_my_posts_comments(user.id)

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

    # add category form
    category_form = CategoryForm()
    if category_form.validate_on_submit():
        category = Category(name=category_form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('You have successfully added a new category', 'success')
        return redirect(url_for('main.profile', username=user.username))

    return render_template("profile/profile.html",
                           user=user,
                           form=form,
                           title=title,
                           password_form=password_form,
                           categories=categories,
                           posts=posts,
                           category_form=category_form,
                           comments=comments
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

        # upload image to cloudinary to specific folder of user
        # image_url = upload(request.files['photo'], folder=str(user.id))['url']
        image_url = upload(request.files['photo'])['url']
        # image_url = upload(
        #     request.files['photo'], folder=current_user.username)['url']
        # image_url = upload(request.files['photo'])['url']

        # filename = photos.save(request.files['photo'])
        # path = f'photos/{filename}'
        user.profile_pic_path = image_url
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

    # sending emails to all users in subscribers table when a new post is created
    # subscribers = Subscriber.query.all()
    # for subscriber in subscribers:
    #     send_email("New post Alert 😃", "emails/new_post", subscriber.email,
    #                user=subscriber, post=post)

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


# delete comment
@main.route('/comment/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    """
        View delete comment function that returns the delete comment page and its data
    """
    comment = Comment.get_comment(id)
    # if comment.user_id != current_user:
    #     abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('You have successfully deleted the comment', 'success')
    return redirect(url_for('main.profile', username=current_user.username))

# update post image


@main.route('/post/<int:id>/update/image', methods=['GET', 'POST'])
@login_required
def update_post_image(id):
    """
        View update post image function that returns the update post image page and its data
    """
    post = Post.query.filter_by(id=id).first()
    if 'photo' in request.files:
        # upload image to cloudinary to specific folder of posts folder
        # image_url = upload(
        #     request.files['photo'], folder=f'posts/{post.id}')['url']
        image_url = upload(request.files['photo'])['url']
        # filename = photos.save(request.files['photo'])
        # path = f'photos/{filename}'
        post.image_path = image_url
        db.session.commit()
        flash('You have successfully uploaded a post image', 'success')
        return redirect(url_for('main.profile', username=current_user.username))


# search posts
@main.route('/search', methods=['GET', 'POST'])
def search():
    """
        View search function that returns the search page and its data
    """
    # get the query string from the search form
    query = request.args.get('query')
    # search for the query string
    posts = Post.get_posts_by_query(query)
    # return the search results
    return render_template('search.html', posts=posts, query=query)


# add users to subscribers list
@main.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    """
         subscribe function that subscribes the user to the post
    """
    email = request.args.get('email')
    new_subscriber = Subscriber(email=email)
    db.session.add(new_subscriber)
    db.session.commit()
    flash('Email submitted successfully', 'success')
    return redirect(url_for('main.index'))
