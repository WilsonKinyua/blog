from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager


# roles table
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

# users table


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # search for user email from user table and check if email already exists
    @classmethod
    def search_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user

    # search for user username from user table and check if username already exists
    @staticmethod
    def search_username(username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user

    def __repr__(self):
        return f'User {self.username}'

# posts category table


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'Category {self.name}'


# posts table
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    title = db.Column(db.String(255))
    content = db.Column(db.String())
    image_path = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(cls):
        posts = Post.query.all()
        return posts

    # get user posts by user id
    @classmethod
    def get_user_posts(cls, user_id):
        posts = Post.query.filter_by(user_id=user_id)
        return posts

    # get post by id
    @classmethod
    def get_post(cls, id):
        post = Post.query.filter_by(id=id).first()
        return post

    # get post by category
    @classmethod
    def get_post_by_category(cls, category_id):
        posts = Post.query.filter_by(category_id=category_id)
        return posts

    # get post comments
    def get_comments(self):
        comments = Comment.query.filter_by(post_id=self.id)
        return comments

    # function to update specific post by id
    # def update_post(self):
    #     db.session.commit()

    # delete post
    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Post {self.title}'


# comments table
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls):
        comments = Comment.query.all()
        return comments

    @classmethod
    def get_comments_by_post(cls, post_id):
        comments = Comment.query.filter_by(post_id=post_id)
        return comments

    # delete comment
    @classmethod
    def delete_comment(cls, id):
        comment = Comment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()

    def __repr__(self):
        return f'Comment {self.content}'

# subscribers table


class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_subscribers(cls):
        subscribers = Subscriber.query.all()
        return subscribers

    def __repr__(self):
        return f'Subscriber {self.email}'
