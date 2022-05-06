import json
import time
import urllib.request
import urllib.parse


GLOBAL_is_first_query = True


def get_api_url_from_query(query):
    # transform the query string into a url-friendly format, and attach it to the scryfall api url
    api_url = 'https://api.scryfall.com/cards/search?q='
    return api_url + urllib.parse.quote_plus(query)


def get_api_data_from_url(url):
    global GLOBAL_is_first_query
    if not GLOBAL_is_first_query:
        # wait 100 milliseconds between calls to avoid spamming the api:  https://scryfall.com/docs/api
        time.sleep(0.1)
    else:
        GLOBAL_is_first_query = False

    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            # error code 404 means the query was processed, but it returned no results
            # here we return None instead of raising an exception because we still want the 'bad' query to be cached
            data = None
        else:
            raise exc

    return data
