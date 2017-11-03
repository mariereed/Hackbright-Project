import requests
import sys
import untangle

reload(sys)
sys.setdefaultencoding('utf-8')

# response = requests.get("http://feeds.feedburner.com/MrMoneyMustache?format=xml")

obj = untangle.parse("mrMoneyRss.xml")

# obj.channel.title





# print response.text
# Prints the XML file
# Why does it kick me out of iPython after this runs?

# ValueError: NO JSON object could be decoded
# Invalid JSON
"""The reason that I can not do this is:
because the request is not being transmitted in JSON,
it is in an XML string (like HTML)"""

"""Import xmltodict or untangle.
untangle returns a python object that mirrors the nodes and attributes
xmltodict ... lookup."""
# Status code is 200 = OK
# r_json = response.json()
