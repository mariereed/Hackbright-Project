# Use this file to add seed data to db
# This should be run only once, if it is re-run then dropdb first

from model import Blog, Article, db, connect_to_db
import xml.etree.ElementTree as ET
from io import StringIO
import requests
import sys
from server import app

# Fixes ascii --> unicode error
reload(sys)
sys.setdefaultencoding('utf-8')


def my_function():
    blog_rss_urls = ["http://feeds.feedburner.com/MrMoneyMustache?format=xml",
                     "http://feeds.feedburner.com/StudyHacks?format=xml",
                     "http://feeds2.feedburner.com/PsychologyBlog?format=xml",
                     "https://www.desmogblog.com/rss.xml",
                     "http://feeds.feedburner.com/readytwowear?format=xml"
                     ]

    # Clean out the tables!
    Blog.query.delete()
    Article.query.delete()

    # Gets all the necessary information for each blog and instantiates
    for blog in blog_rss_urls:
        # Takes a string for blog
        response = requests.get(blog)

        # Create the namespace
        namespace = dict([node for _, node in ET.iterparse(StringIO(response.text), events=['start-ns'])])

        # Parse as element
        root = ET.fromstring(response.text)

        """ Up to this point everything has been consistent.
        I now have to account for differences in the xml files.
        Such as missing information, strange element tags."""

        # If not what two wear:
        if root.find('.//'):
            # All same for name and link
            name = root.find('.//title').text
            rss_url = root.find('.//link').text

            if root.find('.//lastBuildDate'):
                build_date = root.find('.//lastBuildDate').text
                # if what 2 wear.. build_date = ?
                blog = Blog(name=name, rss_url=rss_url, build_date=build_date)
            else:
                blog = Blog(name=name, rss_url=rss_url)

            # Add the blog to the session and commit it
            db.session.add(blog)
            db.session.commit()

            # Now look for the first article for that blog in the RSS feed
            # Check later to make sure the first is actually the newest
            # Doesn't matter for first one, though.

            items = root.findall('.//item')
            first_article = items[0]

            # Gather the needed data, instantiate and commit
            publish_date = first_article.find('.//pubDate').text
            title = first_article.find('.//title').text
            url = first_article.find('.//link').text
            description = first_article.find('.//description').text
            # Might not have content...

            # Works this time because none others have content
            content_obj = first_article.find('content:encoded', namespace)

            article = title

            # ADD CONTENT!
            if content_obj:
                content = content_obj.text()
                article = Article(blog_id=blog.blog_id, title=title, activity=True,
                                  url=url, description=description, content=content,
                                  publish_date=publish_date)
            else:
                article = Article(blog_id=blog.blog_id, title=title, activity=True,
                                  url=url, description=description, publish_date=publish_date)

            db.session.add(article)
            db.session.commit()

        # Else what two wear
        else:
            title = 'title'
            insert = "{" + "{}".format(namespace['']) + "}"
            name = root.find(insert + title).text

            # finding the right link tag (make this a func later)
            link = 'link'
            insert = "{" + "{}".format(namespace['']) + "}"
            links = root.findall(insert + link)
            for link in links:
                if link.get('rel') == "alternate":
                    rss_url = link.get('href')

            published = 'updated'
            insert = "{" + "{}".format(namespace['']) + "}"
            build_date = root.find(insert + published).text

            blog = Blog(name=name, rss_url=rss_url, build_date=build_date)

            db.session.add(blog)
            db.session.commit()

            entry = 'entry'
            insert = "{" + "{}".format(namespace['']) + "}"
            items = root.findall(insert + entry)
            first_article = items[0]

            title = 'title'
            insert = "{" + "{}".format(namespace['']) + "}"
            title = first_article.find(insert + title).text

            # finding the right link tag (make this a func later)
            link = 'link'
            insert = "{" + "{}".format(namespace['']) + "}"
            links = first_article.findall(insert + link)
            for link in links:
                if link.get('rel') == "alternate":
                    url = link.get('href')

            published = 'published'
            insert = "{" + "{}".format(namespace['']) + "}"
            publish_date = first_article.find(insert + published).text

            content = 'content'
            insert = "{" + "{}".format(namespace['']) + "}"
            content = first_article.find(insert + content).text

            article = Article(blog_id=blog.blog_id, title=title, activity=True,
                              url=url, content=content, publish_date=publish_date)

            db.session.add(article)
            db.session.commit()


# ----------------------------------------------------

if __name__ == "__main__":

    connect_to_db(app, "postgresql:///projectdb")

    # In case tables haven't been created, create them
    db.create_all()
    my_function()
