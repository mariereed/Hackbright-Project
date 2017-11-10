from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

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


def my_tag_visible(element):
    # If it is not one of my desired tags
    if element.parent.name not in ['title', 'link', 'description',
                                   'lastBuildDate', 'pubDate', 'content',
                                   'content:encoded', 'updated', 'published',
                                   ]:
        return False
    # If it is a comment
    if isinstance(element, Comment):
        return False
    return True

def within_content_tag_visible(element):
    if element.parent.name not in ['p', 'img', 'div']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def tag_visible(element):
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


# def second_text_from_html(body, tag_vis_funct):
#     soup = BeautifulSoup(body, 'html.parser')
#     texts = soup.findAll({'p': True, 'img': True, 'div': True})
#     visible_texts = filter(tag_vis_funct, texts)
#     visible_texts = [str(t) for t in visible_texts]
#     return " ".join(t.strip() for t in visible_texts)


blog_rss_urls = ["http://feeds.feedburner.com/StudyHacks?format=xml",
                 "http://feeds2.feedburner.com/PsychologyBlog?format=xml",
                 "https://www.desmogblog.com/rss.xml",
                 "http://feeds.feedburner.com/MrMoneyMustache?format=xml",
                 "http://feeds.feedburner.com/readytwowear?format=xml"]

url = blog_rss_urls[4]

page = requests.get(url)

# Provides everything in the content tag
content = text_from_html(page.content, content_tag_visible)

# Provides only the p's, div's, and img's (didn't work for img's)
# next_layer = second_text_from_html(content, within_content_tag_visible)
# c = content.replace('\n', '')
