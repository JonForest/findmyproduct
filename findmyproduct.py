import requests
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

trademeUrl = 'https://www.trademe.co.nz'

class Result:
    def __init__(self, title, price, url):
        self.title = title
        self.price = price
        self.url = url
    

def get_title_details(found_title):
    """
    Receives a BeautifulSoup node and retrieves the details from it
    Returns a Result instance
    """
    try:
        parent = list(found_title.parents)[2] # Will return an `a` tag
        url = trademeUrl + parent['href']
        buy_now = getattr(parent.find(class_='listingBuyNowPrice'), 'string', None)
        current_bid = getattr(parent.find(class_='listingBidPrice'), 'string', None)
        return Result(found_title.string.strip(), buy_now or current_bid, url)
    except AttributeError:
        print(f'Not able to find details for {found_title.string}')


def output_details(results_list):
    for result in results_list:
        print(f'Title: {result.title}')
        print(f'Price: {result.price}')
        print(f'Link: {result.url}')
        print('\n')


def findbook(title):
    page = requests.get(f'{trademeUrl}/Browse/SearchResults.aspx?type=Search&searchType=193&searchString={quote_plus(title)}')
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup(class_='title')

    results = []
    for found_title in titles:
        if title.lower() in found_title.string.strip().lower():
            results.append(get_title_details(found_title))

    return results


def get_titles():
    # Open up the file
    with open('book_list.txt', mode='rt', encoding='utf-8') as f:
        titles = [title.strip() for title in f.readlines()]

    return titles


def main():
    book_titles = get_titles()
    results = []
    for title in book_titles:
        results += findbook(title)

    output_details(results)


if __name__ == '__main__':
    main()