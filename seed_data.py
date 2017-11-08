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

    if tag == 'link':
        links = find_all(node, 'link')

        # If links[0] has no attributes
        if not links[0].get():
            # Follow the else statement below
            if is_normal():
                search_for = './/{}'.format(tag)
            else:
                search_for = normalize_tag(tag)

            return node.find(search_for).text

        for link in links:
            if link.get('rel') == "alternate":
                correct_link = link.get('href')
                return correct_link

    else:
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
        if attrib == 'link':
            # Don't want .text because it is already a string
            tag_values[attrib] = find_tag(node, desired_tag[attrib])
            # Don't do below, return to loop
            continue

        if attrib == 'content':
            content_obj = first_article.find('content:encoded', namespace)
            if content_obj is not None:
                tag_values[attrib] = content_obj.text


        if type(desired_tag[attrib]) is 'list':
            for i in range(len(desired_tag[attrib])):
                if find_tag(node, desired_tag[attrib][i]) is not None:
                    tag_values[attrib] = find_tag(node, desired_tag[attrib][i]).text

            # If for loop completes and still no value for attrib, then set to none
            if not tag_values.get(attrib):
                    tag_values[attrib] = None
        else:
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


def find_entry_tag():
    """Determines the name of the item or entry in the xml file. Returns the correct tag name."""

    if find_all(root, 'item') is not None:
        tag = 'item'
    if find_all(root, 'entry') is not None:
        tag = 'entry'

    return tag


def seed_data():
    """Actually seed the data. """

    for blog in blog_rss_urls:

        response = get_response(blog)
        root = create_root(response)
        namespace = create_namespace(response)

        # For the blog
        desired_tag = {'name': 'title', 'rss_url': 'link', 'build_date': ['lastBuildDate', 'published']}
        tag_values = create_value_dict(root)

        blog = Blog(name=tag_values['name'],
                    rss_url=tag_values['rss_url'],
                    build_date=tag_values['build_date'])

        add_and_commit(blog)

        # For the article
        items = find_all(root, find_entry_tag())
        first_article = items[0]

        desired_tag = {'title': 'title', 'url': 'link', 'publish_date': ['pubDate', 'published'],
                       'description': 'description', 'content': 'content'}

        tag_values = create_value_dict(first_article)
        article = find_tag(first_article, 'title').text

        article = Article(blog_id=blog.blog_id,
                          title=tag_values['title'],
                          activity=True,
                          url=tag_values['url'],
                          description=tag_values['description'],
                          publish_date=tag_values['publish_date'])

        add_and_commit(article)


# ----------------------------------------------------

if __name__ == "__main__":

    connect_to_db(app, "postgresql:///projectdb")

    # In case tables haven't been created, create them
    prep_for_seed()
    db.create_all()
    seed_data()
