from bs4 import BeautifulSoup
from bs4.element import Comment
import requests

desired_tag = {'name': 'title', 'blog_url': 'link', 'build_date': ['lastBuildDate', 'updated'],
                       'title': 'title', 'url': 'link', 'publish_date': ['pubDate', 'published'],
                       'description': 'description', 'content': 'content'}


def content_tag_visible(element):
    # If it is not one of my desired tags
    if element.parent.name not in ['content',
                                   'content:encoded',
                                   ]:
        return False
    # If it is a comment
    if isinstance(element, Comment):
        return False
    return True


def description_tag_visible(element):
    # If it is not one of my desired tags
    if element.parent.name in ['[document]']:
        return True
    if element.parent.name not in ['description']:
        return False
    # If it is a comment
    if isinstance(element, Comment):
        return False
    return True


def tag_visible(element):
    """This is the generic template."""
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body, tag_vis_funct):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_vis_funct, texts)
    return " ".join(t.strip() for t in visible_texts)


blog_rss_urls = ["http://feeds.feedburner.com/StudyHacks?format=xml",
                 "http://feeds2.feedburner.com/PsychologyBlog?format=xml",
                 "https://www.desmogblog.com/rss.xml",
                 "http://feeds.feedburner.com/MrMoneyMustache?format=xml",
                 "http://feeds.feedburner.com/readytwowear?format=xml"]

url = blog_rss_urls[4]

page = requests.get(url)

# Provides everything in the content tags
# sub specific content in for 'page.content'
content = text_from_html(page.content, content_tag_visible)

# Provides everything in the description tags
description = text_from_html(page.content, description_tag_visible)
