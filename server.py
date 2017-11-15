""" The purpose of this file is to run the server."""

from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
import requests
import sys
from model import User, Blog, User_blog, Favorite, Article, connect_to_db, db
from bs import beautify
from datetime import datetime

# from seed_data import

# -------- Set Up ----------------------------------------------
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Raise error for undefined variable
app.jinja_env.undefined = StrictUndefined


# -------- Routes ----------------------------------------------


@app.route('/')
def homepage():
    """ My homepage."""

    return render_template('homepage.html')


@app.route('/login')
def login():
    """ Login page."""

    return render_template('login.html')


@app.route('/log_confirm', methods=["POST"])
def log_confirm():
    """Check whether email and password input matches database."""

    email = request.form.get("email")
    password = request.form.get("password")
    check = User.query.filter(User.email == email).first()

    if check:
        if check.password == password:
            session['user_id'] = check.user_id
            flash('Logged In')
            return redirect('/users/{user_id}'.format(user_id=check.user_id))
        else:
            flash('Incorrect login information')
            return redirect('/login')
    else:
        flash('Incorrect login information')
        return redirect('/login')


@app.route('/register_confirm', methods=["POST"])
def register_confirm():
    """ Allows users to register. Check to make sure they don't already exist."""

    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    check = User.query.filter(User.email == email).first()

    if check:
        flash('{} already exists, please log in.'.format(email))
        return redirect('/login')
    else:
        name = User(name=name,
                         email=email,
                         password=password,
                         user_since=(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                         )

        db.session.add(name)
        db.session.commit()
        flash('Thank you for registering {}'.format(name))
        session['user_id'] = name.user_id
        flash('Logged In')
        return redirect('/users/{user_id}'.format(user_id=name.user_id))


@app.route('/register')
def register():
    """ Registration page."""

    return render_template('register.html')


@app.route('/users/<user_id>')
def display_user_details(user_id):
    """ This page displays the user's details."""

    user = User.query.filter(User.user_id == user_id).first()

    return render_template('user_details.html', user=user)


@app.route('/data')
def display_some_data():
    """ The purpose of this page is to show that data can
    be displayed from projectdb. It displays un-formatted raw data."""

    blogs = Blog.query.all()
    articles = Article.query.all()

    return render_template('data.html', blogs=blogs, articles=articles)


@app.route('/formatted_data')
def display_formatted_data():
    """ The purpose of this page is to test that formatted data displays."""

    articles = Article.query.all()

    formatted_art = [{'content': str(beautify(article.content or '')),
                      'description': str(beautify(article.description or '')),
                      'db_info': article} for article in articles]

    return render_template('data2.html', formatted_art=formatted_art)


# I am not using this... but leaving it for reference.
# @app.route('/return_content.json')
# def return_json():

#     articles = Article.query.all()
#     article_1 = articles[3]

#     new_string = str(beautify(article_1.content))

#     new_content = {'content': new_string}

#     return jsonify(new_content)


@app.route('/timeline')
def display_timeline():
    """Display the timeline with truncated texts and no images."""

    articles = Article.query.all()

    formatted_art = [{'content': str(beautify(article.content or '')),
                      'description': str(beautify(article.description or '')),
                      'db_info': article} for article in articles]

    return render_template('timeline.html', formatted_art=formatted_art)


@app.route('/articles/<article_id>')
def display_article_details(article_id):
    """Display full article content and additional links, information."""

    article = Article.query.get(article_id)

    formatted_art = {'content': str(beautify(article.content or '')),
                     'description': str(beautify(article.description or ''))
                     }

    return render_template('article_details.html', article=article, formatted_art=formatted_art)


# -------- The following is a route template --------------------

# @app.route('/example/<example_id>', methods=['POST'])
# def add_rating_to_db(example_id):
#     """This is an example route to remind me of syntax."""

#     var_from_post = request.form.get('var')

#     var_from_session = session['var']
#     a_query = Class.query.filter(Class.field == var_from_session,
#                          Class.other_field == example_id).first()

#     if a_query:
#         a_query.field = var_from_post
#         db.session.commit()
#     else:
#         new_instance = Class(field1=var_from_post,
#                              session_var=var_from_session,
#                              example_id=example_id)
#         db.session.add(new_instance)
#         db.session.commit()

#     return redirect('/somewhere/{example_id}'.format(example_id=example_id))
#     # or
#     return render_template('somewhere.html', field1=var_from_post,
#                                              session_var=var_from_session,
#                                              example_id=example_id)


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app, 'postgresql:///projectdb')

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
