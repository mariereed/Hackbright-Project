""" The purpose of this file is to fetch data from articles. If checks to
see if there are new articles, if there are it seeds them and updates the
most recent in Blog."""

from model import Article, Blog, db, connect_to_db
from server import app
from seed_data import get_response, create_root, create_namespace, find_all, find_entry_tag, find_tag, create_value_dict, desired_tag


def check_newest_date(blog, new_article_date):
    """ Checks to see if the article is new."""

    if new_article_date > blog.most_recent:
        return True
    else:
        return False


def seed_new_data():
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
                if item is items[0]:
                    temp_most_recent = tag_values['publish_date']

        # UPDATE MOST_RECENT, only to the newest article after all new articles are updated
        this_blog.most_recent = temp_most_recent
        db.session.commit()


if __name__ == "__main__":

    connect_to_db(app, "postgresql:///projectdb")

    seed_new_data()
