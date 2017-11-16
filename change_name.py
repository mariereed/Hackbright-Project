from model import Blog, db, connect_to_db
from server import app


def change_blog_name(blog_id, custom_name):
    """ Creating a custom name for a blog."""

    blog = Blog.query.filter(Blog.blog_id == blog_id).first()

    blog.name = custom_name

    db.session.commit()


if __name__ == "__main__":

    connect_to_db(app, "postgresql:///projectdb")

    change_blog_name(5, 'ReadyTwoWear')
    change_blog_name(1, 'Study Hacks')
	