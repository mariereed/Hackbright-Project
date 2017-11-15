""" The purpose of this file is to provide the beautiful soup logic
that prevents harmful scripts from entering the HTML."""

from bs4 import BeautifulSoup


def beautify(string):

    soup = BeautifulSoup(string, 'html.parser')

    for script in soup(["script", "style"]):
        # If I leave in the "a" it gets some of the links... if i take it out.. i get duplicates.
            script.extract()

    return soup
