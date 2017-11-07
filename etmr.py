import xml.etree.ElementTree as ET
import requests
import sys

# Fixes ascii --> unicode error
reload(sys)
sys.setdefaultencoding('utf-8')

# Request the xml file from the server
response = requests.get("http://feeds.feedburner.com/MrMoneyMustache?format=xml")

# The actual text of the file
# How do I save this to a doc and format it?
response.text

# Parse as element
root = ET.fromstring(response.text)

# # Parse as element tree
# tree = ET.parse('mrMoneyRss.xml')
# root = tree.getroot()

# Define the channel
channel = root.find('.//channel')

# Define all item tags as list
items = channel.findall('.//item')

# Manipulate each item and it's child tags
first_item = items[0]
first_date = first_item.find('.//pubDate')
# To get the actual string timestamp
first_date.text
# >>>Tue, 24 Oct 2017 19:33:38 +0000

# The title of the blog (this is the highest level title in the doc, parent to all items)
blog_title = root.find('.//title')

# The last build date of the XML, this tag is unique
build = root.find('.//lastBuildDate')

# To loop over the items and get the title and publish date for each
for item in items:
    print item.find('.//title').text, item.find('.//pubDate').text
    print

# To do something with the articles titles/dates
for item in items:
    art_title = item.find('.//title').text
    art_date = item.find('.//pubDate').text
    # Do something with these variables

""" From each blog I need to extract the blog title, the last build date (for fast check if the db is up to date.
    As well as for each article I need the title and the publish date for comparing new articles.
    As well as the content needed to display the article on the feed"""

# What content do i need for displaying the article?????
""" Title of the blog, Title of the article, publish date
    Link to the actual article
    Description of article (TLDR)
    The actual article content, including images"""
blog_title = root.find('.//title')
for item in items:
    blog_title = root.find('.//title')
    art_title = item.find('.//title').text
    art_date = item.find('.//pubDate').text
    # link
    description = item.find('.//description').text
    # content
