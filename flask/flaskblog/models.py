from datetime import datetime
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """docstring for User."""

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(25),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(125),
        unique=True,
        nullable=False
    )

    image_file = db.Column(
        db.String(20),
        nullable=False,
        default='default.jpg'
    )

    password = db.Column(
        db.String(60),
        nullable=True
    )

    posts = db.relationship(
        'Post',
        backref='author',
        lazy=True
    )

    comments = db.relationship(
        'Comment',
        backref='author',
        lazy=True
    )

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']

        except Exception:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """docstring for Post."""

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(db.String(200))

    date_posted = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    tags = db.Column(
        db.String(30)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    comments = db.relationship(
        'Comment',
        backref='post',
        lazy=True
    )

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    """docstring for Comment."""

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    date_posted = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id'),
        nullable=False
    )

    def __repr__(self):
        return f"Comment('{self.user_id}', '{self.date_posted}')"
