from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
import requests
import sys
from model import User, Blog, User_blog, Favorite, Article, connect_to_db, db
from bs import beautify
# import bs

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

@app.route('/data')
def display_some_data():
    """ The purpose of this page is to show that data can
    be displayed from projectdb."""

    blogs = Blog.query.all()
    articles = Article.query.all()

    return render_template('data.html', blogs=blogs, articles=articles)

@app.route('/formated_data')
def display_formated_data():
    """ The purpose of this page is to test that formatted data displays."""

    articles = Article.query.all()
    article_1 = articles[0]

    # do stuff to it, then reassign to variables
    new_content = str(beautify(article_1.content))


    return render_template('data2.html', new_content=new_content, article_1=article_1)

@app.route('/return_content.json')
def return_json():

    articles = Article.query.all()
    article_1 = articles[3]

    new_string = str(beautify(article_1.content))

    new_content = {'content': new_string}

    return jsonify(new_content)

@app.route('/test')
def display_it():
    return render_template('testy.html')

@app.route('/test2')
def display_it_2():
    return render_template('testy2.html')

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
