from datetime import datetime
from model import User, User_blog, db, connect_to_db
from server import app


def create_test_user():
    """ Create a user instance and add to db."""

    test_user = User(name="Marie",
                     email="me@marie.com",
                     password="groot",
                     user_since=(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                     )

    db.session.add(test_user)
    db.session.commit()


def follow_blogs(user_id, blog_id):
    """ Allows a user to follow blogs."""

    connection = User_blog(user_id=user_id, blog_id=blog_id)

    db.session.add(connection)
    db.session.commit()


if __name__ == "__main__":

    connect_to_db(app, "postgresql:///projectdb")
