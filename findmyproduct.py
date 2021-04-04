import requests
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

trademeUrl = 'https://www.trademe.co.nz/'

class Result:
    def __init__(self, title, price, url):
        self.title = title
        self.price = price
        self.url = url
    

def _get_title_details(found_title):
    """
    Receives a BeautifulSoup node and retrieves the details from it
    Returns a Result instance
    """
    parent = list(found_title.parents)[3]
    url = trademeUrl + parent.find('a')['href']
    buy_now = parent.find(class_='listingBuyNowPrice').string
    current_bid = parent.find(class_='listingBidPrice').string
    return Result(found_title.string.strip(), buy_now or current_bid, url)


def _output_details(results_list):
    for result in results_list:
        print(f'Title: {result.title}')
        print(f'Price: {result.price}')
        print(f'Link: {result.url}')
        print('\n')


def findbook(title):
    page = requests.get(f'{trademeUrl}Browse/SearchResults.aspx?type=Search&searchType=193&searchString={quote_plus(title)}')
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup(class_='title')

    results = []
    for found_title in titles:
        if title.lower() in found_title.string.strip().lower():
            results.append(_get_title_details(found_title))

    _output_details(results)

if __name__ == '__main__':
    # findbook('From Zero to One')
    # findbook('The Obstacle is the Way')
    # findbook('Outliers')
    findbook('DC Comics Zero Year')