""" The purpose of this file is to run the server."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, g, jsonify, url_for, make_response
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Blog, User_blog, Favorite, Article, connect_to_db, db
from bs import beautify
from bs_old import text_from_html
from datetime import datetime
from functools import wraps, update_wrapper
import bcrypt
import os
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
from datetime import datetime

# -------- Set Up ----------------------------------------------
app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# Raise error for undefined variable
app.jinja_env.undefined = StrictUndefined

# -------- File Upload -----------------------------------------

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = './static/img'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """Checks if an uploaded file is the right type"""

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# -------- Routes ----------------------------------------------


def login_required(decorated_view):
    @wraps(decorated_view)
    def decorated_function(*args, **kwargs):
        if g.current_user is None:
            return redirect('/')
        return decorated_view(*args, **kwargs)
        # I could take this out becuase I don't pass in values
    return decorated_function


# def nocache(view):
#     @wraps(view)
#     def no_cache(*args, **kwargs):
#         response = make_response(view(*args, **kwargs))
#         response.headers['Last-Modified'] = datetime.now()
#         response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#         response.headers['Pragma'] = 'no-cache'
#         response.headers['Expires'] = '-1'
#         return response

    # return update_wrapper(no_cache, view)


@app.before_request
def pre_process_all_requests():
    """Setup the request context"""

    user_id = session.get('user_id')
    if user_id:
        g.current_user = User.query.get(user_id)
        g.logged_in = True
        g.email = g.current_user.email
        g.user_id = g.current_user.user_id
        # Hashed password
        g.password = g.current_user.password
    else:
        g.logged_in = False
        g.current_user = None
        g.email = None


@app.route('/')
def homepage():
    """ My homepage."""

    return render_template('homepage.html', user=g.current_user)


@app.route('/logout')
# @login_required
def logout():
    """ Log out the user."""

    session.clear()

    return redirect('/')


@app.route('/log_confirm', methods=["POST"])
def log_confirm():
    """Check whether email and password input matches database."""

    email = request.form.get("email")
    password = request.form.get("password")
    password = b"{}".format(password)

    check = User.query.filter(User.email == email).first()

    if check:
        if bcrypt.checkpw(password, check.password.encode("utf-8")):
            session['user_id'] = check.user_id
            session['avatar'] = check.avatar
            session['background_img'] = check.background_img
            return redirect('/timeline')
        else:
            flash('Incorrect login information')
            return redirect('/')
    else:
        flash('Incorrect login information')
        return redirect('/')


@app.route('/register_confirm', methods=["POST"])
def register_confirm():
    """ Allows users to register. Check to make sure they don't already exist."""

    email = request.form.get("email")
    name = request.form.get("name")

    password = request.form.get("password")
    password = b"{}".format(password)
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    blogs = request.form.getlist("blog")

    check = User.query.filter(User.email == email).first()

    if check:
        flash('{} already exists, please log in.'.format(email))
        return redirect('/')
    else:
        name = User(name=name,
                    email=email,
                    password=hashed,
                    user_since=(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )

        db.session.add(name)
        db.session.commit()

        for blog in blogs:
            connection = User_blog(user_id=name.user_id, blog_id=int(blog))
            db.session.add(connection)

        db.session.commit()
        session['user_id'] = name.user_id
        session['avatar'] = name.avatar
        session['background_img'] = name.background_img
        return redirect('/dashboard')


@app.route('/dashboard')
@login_required
@nocache
def display_user_details():
    """ This page displays the user's details."""

    # user = User.query.filter(User.user_id == user_id).first()
    users_blogs = User_blog.query.filter(User_blog.user_id == g.user_id).all()

    followed_blogs = []
    for each in users_blogs:
        followed_blogs.append(each.blog)

    all_blogs = Blog.query.all()
    total_blogs = []
    for each in all_blogs:
        total_blogs.append(each)

    not_followed_blogs = []
    for each in total_blogs:
        if each not in followed_blogs:
            not_followed_blogs.append(each)

    favorites = Favorite.query.filter(Favorite.user_id == g.user_id, Favorite.hidden != True).all()
    formatted_art = [{'content': text_from_html(favorite.article.content or ''),
                      'description': text_from_html(favorite.article.description or ''),
                      'db_info': favorite.article} for favorite in favorites]

    faved_ids = [favorite.article_id for favorite in favorites]

    return render_template('user_details.html',
                           user=g.current_user,
                           formatted_art=formatted_art,
                           users_blogs=users_blogs,
                           faved_ids=faved_ids,
                           not_followed_blogs=not_followed_blogs)


@app.route('/change_avatar', methods=["POST"])
@login_required
def change_avatar():
    """Change the avatar for the user."""

    file = request.files['avatar']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user = User.query.filter(User.user_id == g.user_id).first()
        user.avatar = filename

        db.session.commit()
    else:
        if not file:
            flash('No file selected')
        elif not allowed_file(file.filename):
            flash('Invalid file type')
        else:
            flash('Unknown Error')

    return redirect('/dashboard')


@app.route('/change_background', methods=["POST"])
@login_required
def change_background():
    """Change background image for user."""

    file = request.files['background_img']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user = User.query.filter(User.user_id == g.user_id).first()
        user.background_img = filename

        db.session.commit()
    else:
        flash('Invalid file type')

    return redirect('/dashboard')

@app.route('/remove_blog', methods=["POST"])
@login_required
def unfollow_blog():
    """Unfollow a blog."""

    if g.logged_in:
        check = User_blog.query.filter(User_blog.user_id == g.user_id,
                                       User_blog.blog_id == request.form.get('rem_blog')
                                       ).first()
        # If there are records of this blog in user_blogs, then proceed.
        if check:
        # Delete blog for this user.
            blog = User_blog.query.filter(User_blog.user_id == g.user_id,
                                          User_blog.blog_id == request.form.get('rem_blog')).first()

            db.session.delete(blog)
            db.session.commit()
    return redirect('/dashboard')


@app.route('/add_blog', methods=["POST"])
@login_required
def follow_blog():
    """Follow a blog."""

    if g.logged_in:
        check = User_blog.query.filter(User_blog.user_id == g.user_id,
                                       User_blog.blog_id == request.form.get('add_blog')
                                       ).first()
        # If there are no records of this blog in user_blogs, then proceed.
        if not check:
        # Add blog for this user.
            connection = User_blog(user_id=g.user_id, blog_id=request.form.get('add_blog'))

            db.session.add(connection)
            db.session.commit()
    return redirect('/dashboard')


@app.route('/timeline')
@login_required
@nocache
def display_users_timeline():
    """Display the timeline with truncated texts and no images."""

    users_blogs = User_blog.query.filter(User_blog.user_id == g.user_id).all()

    favorites = Favorite.query.filter(Favorite.user_id == g.user_id, Favorite.hidden != True).all()

    faved_ids = [favorite.article_id for favorite in favorites]

    hiddens = Favorite.query.filter(Favorite.user_id == g.user_id, Favorite.hidden == True).all()

    hidden_ids = [favorite.article_id for hidden in hiddens]
    blogs = []
    for item in users_blogs:
        blogs.append(item.blog_id)

    articles = Article.query.filter(Article.blog_id.in_(blogs),
                                    db.not_(Article.article_id.in_(hidden_ids))
                                            ).order_by(Article.publish_date.desc()
                                    ).all()
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
            favorite = Favorite(user_id=g.user_id, article_id=request.form.get('articleId'))

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
            favorite = Favorite.query.filter(Favorite.user_id == g.user_id,
                                             Favorite.article_id == request.form.get('articleId')
                                             ).first()

            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'confirm': True, 'id': request.form.get('articleId')})
        else:
            return jsonify({'confirm': 'False'})


@app.route('/hide', methods=["POST"])
@login_required
def hide_an_article():
    """Hide an article from the timeline."""
    article_id = request.form.get('articleId')[5:]

    if g.logged_in:
        check = Favorite.query.filter(Favorite.user_id == g.user_id,
                                      Favorite.article_id == article_id
                                      ).first()
        # If there are no records of this articles in favorites, then proceed.
        if not check:
        # Create a favorite from the ajax request
            favorite = Favorite(user_id=g.user_id, article_id=article_id, hidden=True)

            db.session.add(favorite)
            db.session.commit()
            return jsonify({'confirm': True, 'id': article_id})
        else:
            check.hidden = True
            db.session.commit()
            return jsonify({'confirm': True, 'id': article_id})


@app.route('/articles/<article_id>')
@nocache
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
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
