import urllib.request
import json
from .models import Quote


def process_results(quote_list):
    """
        Processes the results from the API call.
    """
    quotes = []
    for quote in quote_list:
        author = quote.get('author')
        quote = quote.get('quote')
        quotes.append(Quote(author, quote))
    return quotes


# function to get quote from API
def get_quotes():
    """
        Gets the quotes from the API.
    """
    url = 'http://quotes.stormconsultancy.co.uk/random.json'
    with urllib.request.urlopen(url) as response:
        quote_list = json.loads(response.read())
    return process_results(quote_list)
