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


def get_title_details(found_title, acceptable_price=50):
    """
    Receives a BeautifulSoup node and retrieves the details from it
    Returns a Result instance
    """
    try:
        parent = list(found_title.parents)[2] # Will return an `a` tag
        url = trademeUrl + parent['href']
        buy_now = getattr(parent.find(class_='listingBuyNowPrice'), 'string', None)
        current_bid = getattr(parent.find(class_='listingBidPrice'), 'string', None)
    except AttributeError:
        print(f'Not able to find details for {found_title.string}')
        return None

    try:
        price = buy_now or current_bid
        if float(price[1:]) > acceptable_price:
            return None
    except ValueError:
        print(f'Not able to cast price to float for {found_title.string}')

    return Result(found_title.string.strip(), buy_now or current_bid, url)

def output_details(results_list):
    for result in results_list:
        print(f'Title: {result.title}')
        print(f'Price: {result.price}')
        print(f'Link: {result.url}')
        print('\n')


def findbook(title_price):
    """
    Accepts a tuple of title and price
    Returns a list of Result objects
    """

    title = title_price[0]
    page = requests.get(f'{trademeUrl}/Browse/SearchResults.aspx?type=Search&searchType=193&searchString={quote_plus(title)}')
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup(class_='title')

    results = []
    for found_title in titles:
        if title.lower() in found_title.string.strip().lower():
            result = get_title_details(found_title, title_price[1])
            if result:
                results.append(result)

    return results


def get_titles_and_prices():
    """
    Returns a list of tuples in the format [(title,price), (title, price)...]
    """
    # Open up the file
    with open('book_list.txt', mode='rt', encoding='utf-8') as f:
        books = []
        try:
            books = [(book.split('-')[0].strip(), float(book.split('-')[1].strip())) for book in f.readlines()]
        except IndexError:
            print('Error in format of book_list.txt. All books should be <book_title(string)>-<price(number)>')
        except ValueError:
            print('Price should be formatted without the $, e.g. 15.00 or 15, not $15')
        finally:
            return books



def main():
    book_titles = get_titles_and_prices()
    results = []
    for title in book_titles:
        results += findbook(title)

    output_details(results)


if __name__ == '__main__':
    main()