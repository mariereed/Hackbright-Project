from datetime import datetime
from model import User, User_blog, db, connect_to_db
from server import app


def create_test_user(name, email, password):
    """ Create a user instance and add to db."""

    test_user = User(name=name,
                     email=email,
                     password=password,
                     user_since=(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                     )

    db.session.add(test_user)
    db.session.commit()


def follow_blogs(user_id, blog_id):
    """ Allows a user to follow blogs."""

    connection = User_blog(user_id=user_id, blog_id=blog_id)

    db.session.add(connection)
    db.session.commit()


def check_newest_date(blog_id, new_article_date):
    """ Checks the db for the newest article publish date and sets it in blogs."""

    blog = Blog.query.filter(Blog.blog_id == blog_id).first()

    if datetime.strptime(new_article_date, "%Y-%m-%d %H:%M:%S") > datetime.strptime(blog.most_recent, "%Y-%m-%d %H:%M:%S"):
        # add the new article into the database, set most recent to


if __name__ == "__main__":

    connect_to_db(app, "postgresql:///projectdb")

    # create_test_user("Marie", "me@marie.com", "groot")
    # create_test_user("Marie's Friend", "me@friend.com", "root")
    # create_test_user("Ghost", "me@boo.com", "boo")

    # follow_blogs(1, 1)
    # follow_blogs(1, 2)
    # follow_blogs(1, 3)
    # follow_blogs(1, 4)
    # follow_blogs(1, 5)
    # follow_blogs(2, 1)
    # follow_blogs(2, 4)
    # follow_blogs(3, 2)
    # follow_blogs(3, 3)
    # follow_blogs(3, 5)
