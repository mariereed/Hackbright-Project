from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
import requests
import sys
from model import User, Blog, User_blog, Favorite, Article, connect_to_db, db

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

    blog = Blog.query.filter(Blog.name == 'Mr. Money Mustache').first()

    render_template('data.html', blog=blog)


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
