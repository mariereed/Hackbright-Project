"""Models and database functions for my project."""

from flask_sqlalchemy import SQLAlchemy
import sys
# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()
reload(sys)
sys.setdefaultencoding('utf-8')
##############################################################################
# Model definitions


class User(db.Model):
    """Users of my website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    user_since = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "< User name: {} >".format(self.name)


class Blog(db.Model):
    """Blogs which my users follow."""

    __tablename__ = "blogs"

    blog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rss_url = db.Column(db.String(200), nullable=False)
    blog_url = db.Column(db.String(200), nullable=False)
    build_date = db.Column(db.String(200), nullable=True)
    most_recent = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "< Blog name: {} >".format(self.name)


class Article(db.Model):
    """Articles from rss feeds of blogs that my users follow."""

    __tablename__ = "articles"

    article_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'))
    title = db.Column(db.String(500), nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(500), nullable=False)
    activity = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(50000), nullable=True)
    content = db.Column(db.String(1000000), nullable=True)

    # Define relationship to blog
    blog = db.relationship("Blog", backref='blogs')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "< Article title: {} >".format(self.title)


class Favorite(db.Model):
    """Favorited articles of my users."""

    __tablename__ = "favorites"

    fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.article_id'), unique=True, nullable=False)

    # Define relationship to user
    user = db.relationship("User", backref='favorites')

    # Define relationship to article
    article = db.relationship("Article", backref='favorites')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Favorite article: {}>".format(self.article.title)


class User_blog(db.Model):
    """Association table between users and blogs."""

    __tablename__ = "user_blogs"

    user_blog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'), nullable=False)

    # Define relationship to user
    user = db.relationship("User", backref='user_blogs')

    # Define relationship to blog
    blog = db.relationship("Blog", backref='user_blogs')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Blog_user User: {} Blog: {}>".format(self.user.name, self.blog.title)


##############################################################################
# Helper functions

def connect_to_db(app, db_uri):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app, 'postgresql:///projectdb')
