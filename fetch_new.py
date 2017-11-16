""" The purpose of this file is to fetch data from articles. If checks to
see if there are new articles, if there are it seeds them and updates the
most recent in Blog."""

from model import Article, Blog, db, connect_to_db
from server import app
from seed_data import get_response, create_root, create_namespace, find_all, find_entry_tag, find_tag, create_value_dict, desired_tag
from datetime import datetime


def check_newest_date(blog, new_article_date):
    """ Checks to see if the article is new."""

    if "-" in new_article_date:
        new_article_date = datetime.strptime(new_article_date[:-10], "%Y-%m-%dT%H:%M:%S")
    else:
        new_article_date = datetime.strptime(new_article_date[:-6], "%a, %d %b %Y %H:%M:%S")
    if new_article_date > blog.most_recent:
        # THIS ISNT WORKING
        # DOES NOT WORK FOR DESMOG BLOG most_recent is very old. order may be wrong ?
        """ This is happening becausae FREAKING desmogblog
        claims its most recent article is from nov 24 2016!!!!"""
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
        temp_most_recent = None
        for item in items:
            tag_values = create_value_dict(item, desired_tag, namespace)
            pub_date = tag_values['publish_date']
            print 'test'
            if check_newest_date(this_blog, pub_date):
            # This line above appears not to be working either...
            # the comparison is basically doing everyonther one.
                # # THEN SEED THE ARTICLE
                # article = find_tag(item, 'title', namespace).text
                # article = Article(blog_id=this_blog.blog_id,
                #                   title=tag_values['title'],
                #                   activity=True,
                #                   url=tag_values['url'],
                #                   description=tag_values['description'],
                #                   publish_date=tag_values['publish_date'],
                #                   content=tag_values['content'])
                # db.session.add(article)
                # if item is items[0]:
                #     temp_most_recent = db.DateTime(tag_values['publish_date'])
                print
                print
                print 'I FOUND SOMETHING NEWWWWWWWW'
                print
                print
        # UPDATE MOST_RECENT, only to the newest article after all new articles are updated
        # if temp_most_recent:
        #     this_blog.most_recent = temp_most_recent
        # db.session.commit()
    print 'finished'


if __name__ == "__main__":

    connect_to_db(app, "postgresql:///projectdb")

    seed_new_data()
