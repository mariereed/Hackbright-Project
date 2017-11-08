# Use this file to add seed data to db
# This should be run only once, if it is re-run then dropdb first

from model import Blog, Article, db, connect_to_db
import xml.etree.ElementTree as ET
from io import StringIO
import requests
import sys
from server import app


blog_rss_urls = ["http://feeds.feedburner.com/MrMoneyMustache?format=xml",
                 "http://feeds.feedburner.com/StudyHacks?format=xml",
                 "http://feeds2.feedburner.com/PsychologyBlog?format=xml",
                 "https://www.desmogblog.com/rss.xml",
                 "http://feeds.feedburner.com/readytwowear?format=xml"
                 ]


def prep_for_seed():
    """All the steps necessary to start the seeding."""

    # Fixes ascii --> unicode error
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # Clean out the tables!
    Blog.query.delete()
    Article.query.delete()


def get_response(blog):
    """Sends a request to a blog url, returns the response."""

    response = requests.get(blog)

    return response


def create_root(response):
    """Creates and returns the ElementTree root."""

    root = ET.fromstring(response.text)

    return root


def create_namespace(response):
    """Create the namespace."""

    namespace = dict(
        [node for _, node in ET.iterparse(
            StringIO(response.text), events=['start-ns']
            )]
        )

    return namespace


def normalize_tag(tag):
    """When a blog parses oddly and requires special formatting,
    this is one of the solutions. Returns the formatted root.find.
    Should be used in another function to find at specific node.
    """

    insert = "{" + "{}".format(namespace['']) + "}"
    search_for = insert + tag
    return search_for


def find_tag(node, tag):
    """Takes in a node (ie: root) and an element tag, returns the text."""
    if is_normal():
        search_for = './/{}'.format(tag)
    else:
        search_for = normalize_tag(tag)

    return node.find(search_for)


def is_normal():
    if root.find('.//'):
        return True
    else:
        return False


def create_value_dict(node):
    """Creates a attrib-value dictionary for instantiating each instance object."""

    tag_values = {}

    for attrib in desired_tag:
        if find_tag(node, desired_tag[attrib]) is not None:
            tag_values[attrib] = find_tag(node, desired_tag[attrib]).text
        else:
            tag_values[attrib] = None

    return tag_values


def add_and_commit(instance_type):
    """Adds and commits the instance into the db."""

    db.session.add(instance_type)
    db.session.commit()

    return "Added and committed!"


def find_all(node, tag):
    """Find all of a certain tag from node."""

    if is_normal():
        search_for = './/{}'.format(tag)
    else:
        search_for = normalize_tag(tag)

    return node.findall(search_for)


def seed_data():
    """Actually seed the data. """

    for blog in blog_rss_urls:

        response = get_response(blog)
        root = create_root(response)
        namespace = create_namespace(response)

        desired_tag = {'name': 'title', 'rss_url': 'link', 'build_date': 'lastBuildDate'}

        # DOES NOT ACCOUNT FOR WHAT 2 WEAR
        # How do I have multiple options for build_date? a list?
        # Maybe I'll just have to look for date like things.
        create_value_dict(root)

        blog = Blog(name=desired_tag['name'],
                    rss_url=desired_tag['rss_url'],
                    build_date=desired_tag['build_date'])

        add_and_commit(blog)

        # Now look for the first article for that blog in the RSS feed
        # Check later to make sure the first is actually the newest
        # Doesn't matter for first one, though.

        items = find_all(root, 'item')
        first_article = items[0]

        desired_tag = {'title': 'title', 'url': 'link', 'publish_date': 'pubDate', 'description': 'description'}

        create_value_dict(first_article)

        article = find_tag(first_article, 'title').text

        article = Article(blog_id=blog.blog_id,
                          title=desired_tag['title'],
                          activity=True,
                          url=desired_tag['url'],
                          description=desired_tag['description'],
                          publish_date=desired_tag['publish_date'])

        # content_obj = first_article.find('content:encoded', namespace)
        # # ADD CONTENT!
        # if content_obj is not None:
        #     content = content_obj.text
        #     article = Article(blog_id=blog.blog_id, title=title, activity=True,
        #                       url=url, description=description, content=content,
        #                       publish_date=publish_date)
        # else:
        #     article = Article(blog_id=blog.blog_id, title=title, activity=True,
        #                       url=url, description=description, publish_date=publish_date)

        add_and_commit(article)

        # # Else what two wear
        # else:
        #     title = 'title'
        #     insert = "{" + "{}".format(namespace['']) + "}"
        #     name = root.find(insert + title).text

        #     # finding the right link tag (make this a func later)
        #     link = 'link'
        #     insert = "{" + "{}".format(namespace['']) + "}"
        #     links = root.findall(insert + link)
        #     for link in links:
        #         if link.get('rel') == "alternate":
        #             rss_url = link.get('href')

        #     published = 'updated'
        #     insert = "{" + "{}".format(namespace['']) + "}"
        #     build_date = root.find(insert + published).text

        #     blog = Blog(name=name, rss_url=rss_url, build_date=build_date)

        #     db.session.add(blog)
        #     db.session.commit()

        #     entry = 'entry'
        #     insert = "{" + "{}".format(namespace['']) + "}"
        #     items = root.findall(insert + entry)
        #     first_article = items[0]

        #     title = 'title'
        #     insert = "{" + "{}".format(namespace['']) + "}"
        #     title = first_article.find(insert + title).text

        #     # finding the right link tag (make this a func later)
        #     link = 'link'
        #     insert = "{" + "{}".format(namespace['']) + "}"
        #     links = first_article.findall(insert + link)
        #     for link in links:
        #         if link.get('rel') == "alternate":
        #             url = link.get('href')

        #     published = 'published'
        #     insert = "{" + "{}".format(namespace['']) + "}"
        #     publish_date = first_article.find(insert + published).text

        #     content = 'content'
        #     insert = "{" + "{}".format(namespace['']) + "}"
        #     content = first_article.find(insert + content).text

        #     article = Article(blog_id=blog.blog_id, title=title, activity=True,
        #                       url=url, content=content, publish_date=publish_date)

        #     db.session.add(article)
        #     db.session.commit()


# ----------------------------------------------------

if __name__ == "__main__":

    connect_to_db(app, "postgresql:///projectdb")

    # In case tables haven't been created, create them
    prep_for_seed()
    db.create_all()
    seed_data()

