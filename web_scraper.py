"""
CSC111: web_scraper
This module contains methods pertaining to scraping the links that are passed in from the user in order to retreive
HTML data, and parse it into a dictionary that will be inputted to the GraphMethods module in order to generate
a WIKILINK graph.
This file is Copyright (c) 2023 Arjun Sohal, Mani Tahami.
"""
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from requests import get


def get_url(url: str) -> dict | None:
    """
    Retrieves links from the HTML content of a web page.
    Preconditions:
    - The `url` parameter must be a string representing a valid URL.
    """
    request = get(url)
    if request.status_code != 200:
        print('Error, request status code of {}'.format(request.status_code))
        return None

    weburl = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(weburl).read()

    soup = BeautifulSoup(data, "html.parser")

    return getlinks(soup)


def getlinks(soup: BeautifulSoup) -> dict:
    """
    Extracts links from a BeautifulSoup object representing an HTML document,
    filtering out links that are not relevant for our purposes.

    Preconditions:
    - The `soup` parameter must be a BeautifulSoup object representing an HTML document.
    """
    alllinks = soup.find(id="bodyContent").find_all("a")
    linkdict = {}
    for x in alllinks:
        x = str(x)
        if '<a href="/wiki/' in x and not (
                '<a href="/wiki/Special:BookSources' in x or '<a href="/wiki/Category' in x or '/wiki/Help' in x):
            start = x.find('/')
            end = x.find(' title') - 1
            x = 'https://en.wikipedia.org' + x[start:end]
            if x not in linkdict:
                linkdict[x] = 1
            else:
                linkdict[x] += 1

    return get_top_occurences(linkdict)


def get_top_occurences(items: dict) -> dict:
    """
    Takes a dictionary of items and returns a new dictionary containing the top 10 most frequently occurring items.

    Preconditions:
    - The `items` parameter must be a dictionary with string keys and integer values representing
      the number of occurrences of a specific Wikipedia link name.
    """
    sorted_dict = sorted(items.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_dict) > 10:
        sorted_dict = sorted_dict[:10]
    converted_dict = dict(sorted_dict)
    return converted_dict
