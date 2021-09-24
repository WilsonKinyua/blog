from flask import render_template, redirect, url_for, abort, flash, request
from . import main
from flask_login import login_required, current_user
from ..models import User, Role, Post, Comment, Category
from .. import db, photos
# from .forms import UpdateProfileForm, CommentForm, CategoryForm
from slugify import slugify


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

    return render_template('index.html', posts=posts, categories=categories)
