from datetime import datetime
from model import Article, Blog, db, connect_to_db
from server import app
from seed_data import get_response, create_root, create_namespace, find_all, find_entry_tag, find_tag, create_value_dict, desired_tag


def check_newest_date(blog, new_article_date):
    """ Checks to see if the article is new."""

    if datetime.strptime(new_article_date, "%Y-%m-%d %H:%M:%S") > datetime.strptime(blog.most_recent, "%Y-%m-%d %H:%M:%S"):
        return True
    else:
        return False


def seed_data():
    """ Fetch the articles and add into db if it is new. """

    blog_rss_urls = ["http://feeds.feedburner.com/StudyHacks?format=xml",
                     "http://feeds2.feedburner.com/PsychologyBlog?format=xml",
                     "https://www.desmogblog.com/rss.xml",
                     "http://feeds.feedburner.com/MrMoneyMustache?format=xml",
                     "http://feeds.feedburner.com/readytwowear?format=xml"]

    for blog in blog_rss_urls:

        response = get_response(blog)
        root = create_root(response)
        namespace = create_namespace(response)

        items = find_all(root, find_entry_tag(root, namespace), namespace)
        this_blog = Blog.query.filter(Blog.rss_url == blog).first()

        for item in items:
            tag_values = create_value_dict(item, desired_tag, namespace)
            pub_date = tag_values['publish_date']
            if check_newest_date(this_blog, pub_date):
                # THEN SEED THE ARTICLE
                article = find_tag(item, 'title', namespace).text
                article = Article(blog_id=this_blog.blog_id,
                                  title=tag_values['title'],
                                  activity=True,
                                  url=tag_values['url'],
                                  description=tag_values['description'],
                                  publish_date=tag_values['publish_date'],
                                  content=tag_values['content'])
                db.session.add(article)
                # UPDATE MOST_RECENT
                this_blog.most_recent = tag_values['publish_date']
                db.session.commit()
            # ELSE: MOVE ON TO THE NEXT ONE


if __name__ == "__main__":

    connect_to_db(app, "postgresql:///projectdb")
