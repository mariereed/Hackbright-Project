"""Provides text only, used for making the truncated article descriptions. """
from bs4 import BeautifulSoup
from bs4.element import Comment


def tag_visible(element):
    """This is the generic template."""
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)
