from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import pandas as pd
import random

website = 'https://en.wikipedia.org/wiki/Canada'
website_list = [website]
pages = []
souplist = []
last_page = False


def get_url(url):
    request = requests.get(website_list[-1])
    if request.status_code != 200:
        print('Error, request status code of {}'.format(request.status_code))
        return None

    pages.append(request)

    weburl = Request(website, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(weburl).read()

    soup = BeautifulSoup(data, "html.parser")
    souplist.append(soup)

    getURLs(souplist)


def getURLs(souplist):
    allLinks = souplist[-1].find(id="bodyContent").find_all("a")
    linkdict = {}
    for x in allLinks:
        x = str(x)
        if '<a href="/wiki/' in x and not ('<a href="/wiki/Special:BookSources' in x or '<a href="/wiki/Category' in x):
            start = x.find('/')
            end = x.find(' title') - 1
            x = x[start:end]
            if x not in linkdict:
                linkdict[x] = 1
            else:
                linkdict[x] += 1

    print(linkdict)


print(get_url(website))
