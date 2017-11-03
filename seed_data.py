# Use this file to add seed data to db

from model import User, Blog, Article, User_blog, Favorite, db, connect_to_db
import datetime as dt
import xml.etree.ElementTree as ET
import requests
import sys
from server import app

# Fixes ascii --> unicode error
reload(sys)
sys.setdefaultencoding('utf-8')


blog_rss_urls = ["http://feeds.feedburner.com/MrMoneyMustache?format=xml"]

# Gets all the necessary information for each blog and instantiates
for blog in blog_rss_urls:
    # Takes a string for blog
    response = requests.get(blog)

    # Parse as element
    root = ET.fromstring(response.text)

    # Define all fields for Blog
    build_date = root.find('.//lastBuildDate').text
    name = root.find('.//title').text
    rss_url = root.find('.//link').text

    # Insantiate the blog
    blog = Blog(name=name, rss_url=rss_url, build_date=build_date)

    # Add the blog to the session and commit it
    db.session.add(blog)
    db.session.commit()

    # Now look for the first article in the RSS feed
    channel = root.find('.//channel')
    items = channel.findall('.//item')
    first_article = items[0]

    # Gather the needed data, instantiate and commit
    publish_date = first_article.find('.//pubDate').text
    title = first_article.find('.//title').text
    url = first_article.find('.//link').text
    description = first_article.find('.//description').text
    content = first_article.find('.//content:encoded').text

    article = Article(blog_id=blog_id, title=title, activity=True,
                      url=url, description=description, content=content,
                      publish_date=publish_date)
    db.session.add(article)
    db.session.commit()







