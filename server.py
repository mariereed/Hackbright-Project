""" The purpose of this file is to run the server."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Blog, User_blog, Favorite, Article, connect_to_db, db
from bs import beautify
from bs_old import text_from_html
from datetime import datetime
from functools import wraps

# -------- Set Up ----------------------------------------------
app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# Raise error for undefined variable
app.jinja_env.undefined = StrictUndefined

# -------- Routes ----------------------------------------------


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.current_user is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def pre_process_all_requests():
    """Setup the request context"""

    user_id = session.get('user_id')
    if user_id:
        g.current_user = User.query.get(user_id)
        g.logged_in = True
        g.email = g.current_user.email
        g.user_id = g.current_user.user_id
        g.password = g.current_user.password
    else:
        g.logged_in = False
        g.current_user = None
        g.email = None


@app.route('/')
def homepage():
    """ My homepage."""

    return render_template('homepage.html')


@app.route('/login')
def login():
    """ Login page."""

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """ Log out the user."""

    session.clear()

    return redirect('/')


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
    blogs = request.form.getlist("blog")

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

        for blog in blogs:
            connection = User_blog(user_id=name.user_id, blog_id=int(blog))
            db.session.add(connection)

        db.session.commit()
        flash('Thank you for registering {}'.format(name.name))
        session['user_id'] = name.user_id
        flash('Logged In')
        return redirect('/users/{user_id}'.format(user_id=name.user_id))


@app.route('/register')
def register():
    """ Registration page."""

    return render_template('register.html')


@app.route('/users/<user_id>')
@login_required
def display_user_details(user_id):
    """ This page displays the user's details."""

    # user = User.query.filter(User.user_id == user_id).first()
    users_blogs = User_blog.query.filter(User_blog.user_id == user_id).all()

    return render_template('user_details.html', user=g.current_user, users_blogs=users_blogs)


@app.route('/remove_blog', methods=["POST"])
@login_required
def unfollow_blog():
    """Unfollow a blog."""

    if g.logged_in:
        check = User_blog.query.filter(User_blog.user_id == g.user_id,
                                       User_blog.blog_id == request.form.get('blog')
                                       ).first()
        # If there are records of this blog in user_blogs, then proceed.
        if check:
        # Delete blog for this user.
            blog = User_blog.query.filter(User_blog.user_id == g.user_id, User_blog.blog_id == request.form.get('blog')).first()

            db.session.delete(blog)
            db.session.commit()
    return redirect('/users/{user_id}'.format(user_id=g.user_id))


@app.route('/timeline/<user_id>')
@login_required
def display_users_timeline(user_id):
    """Display the timeline with truncated texts and no images."""

    users_blogs = User_blog.query.filter(User_blog.user_id == user_id).all()

    favorites = Favorite.query.filter(Favorite.user_id == user_id).all()

    faved_ids = [favorite.article_id for favorite in favorites]

    blogs = []
    for item in users_blogs:
        blogs.append(item.blog_id)

    articles = Article.query.filter(Article.blog_id.in_(blogs)).order_by(Article.publish_date.desc()).all()
    # Here i need to order the articles by publish date

    formatted_art = [{'content': text_from_html(article.content or ''),
                      'description': text_from_html(article.description or ''),
                      'db_info': article} for article in articles]

    return render_template('users_timeline.html',
                           user=g.current_user,
                           formatted_art=formatted_art,
                           users_blogs=users_blogs,
                           faved_ids=faved_ids
                           )


@app.route('/favorites/<user_id>')
@login_required
def display_users_favorites(user_id):
    """Display the timeline with truncated texts and no images."""

    users_blogs = User_blog.query.filter(User_blog.user_id == user_id).all()

    blogs = []
    for item in users_blogs:
        blogs.append(item.blog_id)

    favorites = Favorite.query.filter(Favorite.user_id == user_id).all()
    # .order_by(Favorite.article.publish_date.desc())
    formatted_art = [{'content': text_from_html(favorite.article.content or ''),
                      'description': text_from_html(favorite.article.description or ''),
                      'db_info': favorite.article} for favorite in favorites]

    faved_ids = [favorite.article_id for favorite in favorites]

    return render_template('users_favorites.html',
                           user=g.current_user,
                           formatted_art=formatted_art,
                           users_blogs=users_blogs,
                           faved_ids=faved_ids
                           )


@app.route('/like', methods=["POST"])
@login_required
def like_an_article():
    """Favorite an article."""

    if g.logged_in:
        check = Favorite.query.filter(Favorite.user_id == g.user_id,
                                      Favorite.article_id == request.form.get('articleId')
                                      ).first()
        # If there are no records of this articles in favorites, then proceed.
        if not check:
        # Create a favorite from the ajax request
            favorite = Favorite(user_id=session['user_id'], article_id=request.form.get('articleId'))

            db.session.add(favorite)
            db.session.commit()
            return jsonify({'confirm': True, 'id': request.form.get('articleId')})
        else:
            return jsonify({'confirm': 'False'})
    # else:
    #     return jsonify({'confirm': 'False'})


@app.route('/unlike', methods=["POST"])
@login_required
def unlike_an_article():
    """Unfavorite an article."""

    if g.logged_in:
        check = Favorite.query.filter(Favorite.user_id == g.user_id,
                                      Favorite.article_id == request.form.get('articleId')
                                      ).first()
        # If there are records of this article in favorites, then proceed.
        if check:
        # Create a favorite from the ajax request
            favorite = Favorite.query.filter(Favorite.user_id == session['user_id'], Favorite.article_id == request.form.get('articleId')).first()

            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'confirm': True, 'id': request.form.get('articleId')})
        else:
            return jsonify({'confirm': 'False'})


@app.route('/articles/<article_id>')
def display_article_details(article_id):
    """Display full article content and additional links, information."""

    article = Article.query.get(article_id)

    formatted_art = {'content': str(beautify(article.content or '')),
                     'description': str(beautify(article.description or ''))
                     }

    return render_template('article_details.html', article=article, formatted_art=formatted_art)


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app, 'postgresql:///projectdb')

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
