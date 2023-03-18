from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen

website = 'https://en.wikipedia.org/wiki/University_of_Toronto'


def get_url(url):
    request = requests.get(url)
    if request.status_code != 200:
        print('Error, request status code of {}'.format(request.status_code))
        return None

    weburl = Request(website, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(weburl).read()

    soup = BeautifulSoup(data, "html.parser")

    getLinks(soup)


def getLinks(soup):
    allLinks = soup.find(id="bodyContent").find_all("a")
    linkdict = {}
    for x in allLinks:
        x = str(x)
        if '<a href="/wiki/' in x and not (
                '<a href="/wiki/Special:BookSources' in x or '<a href="/wiki/Category' in x or '/wiki/Help' in x):
            start = x.find('/')
            end = x.find(' title') - 1
            x = x[start:end]
            if x not in linkdict:
                linkdict[x] = 1
            else:
                linkdict[x] += 1

    print(getTopOccurences(linkdict))


def getTopOccurences(items: dict) -> dict:
    sorted_dict = sorted(items.items(), key=lambda x: x[1], reverse=True)
    converted_dict = dict(sorted_dict)
    final_dict = {}
    for item in converted_dict:
        final_dict[item] = converted_dict[item]
        if len(final_dict) == 10:
            return final_dict
    return final_dict

