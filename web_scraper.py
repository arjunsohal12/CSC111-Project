from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen

website = 'https://en.wikipedia.org/wiki/Canada'
last_page = False


def get_url(url: str) -> dict:
    request = requests.get(url)
    if request.status_code != 200:
        print('Error, request status code of {}'.format(request.status_code))
        return None

    weburl = Request(website, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(weburl).read()

    soup = BeautifulSoup(data, "html.parser")

    return getlinks(soup)


def getlinks(soup: BeautifulSoup) -> dict:
    alllinks = soup.find(id="bodyContent").find_all("a")
    linkdict = {}
    for x in alllinks:
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

    return getTopOccurences(linkdict)


def getTopOccurences(items: dict) -> dict:
    top_occurences = items.values()
    list_of_values = set(top_occurences)
    list_of_values = list(list_of_values)
    list_of_values.sort(reverse=True)
    final_dict = {}
    for i in range(len(list_of_values)):
        for item in items:
            if items[item] == list_of_values[i]:
                final_dict[item] = items[item]
                if len(final_dict) == 10:
                    return final_dict

    return final_dict
