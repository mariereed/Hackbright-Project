""" The purpose of this file is to fetch data from articles. If checks to
see if there are new articles, if there are it seeds them and updates the
most recent in Blog."""

from model import Article, Blog, db, connect_to_db
from server import app
from seed_data import get_response, create_root, create_namespace, find_all, find_entry_tag, find_tag, create_value_dict, desired_tag
from datetime import datetime
import schedule
import time


def check_newest_date(blog, new_article_date):
    """ Checks to see if the article is new."""

    if "-" in new_article_date:
        new_article_date = datetime.strptime(new_article_date[:-10], "%Y-%m-%dT%H:%M:%S")
    else:
        new_article_date = datetime.strptime(new_article_date[:-6], "%a, %d %b %Y %H:%M:%S")
    if new_article_date > blog.most_recent:
        return True
    else:
        return False


def job():
    """Fetch the articles and add into db if it is new."""

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
            if check_newest_date(this_blog, pub_date):
                article = find_tag(item, 'title', namespace).text
                article = Article(blog_id=this_blog.blog_id,
                                  title=tag_values['title'],
                                  activity=True,
                                  url=tag_values['url'],
                                  description=tag_values['description'],
                                  publish_date=tag_values['publish_date'],
                                  content=tag_values['content'])
                db.session.add(article)
                print "Added article: ", tag_values['title']
                if item is items[0] and this_blog.blog_id != 3:
                    temp_most_recent = tag_values['publish_date']
                if this_blog.blog_id == 3 and item is items[1]:
                    temp_most_recent = tag_values['publish_date']
        if temp_most_recent:
            this_blog.most_recent = temp_most_recent
            print "Updating most_recent, id:", this_blog.blog_id
        db.session.commit()


if __name__ == "__main__":

    connect_to_db(app, "postgresql:///projectdb")

    schedule.every(1).hour.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
