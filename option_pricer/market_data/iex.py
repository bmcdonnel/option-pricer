"""
Market Data module using IEX Trading's free API.
"""

from datetime import datetime

import logging
import requests

from option_pricer.market_data.quote import Quote

URL = "https://api.iextrading.com/1.0"

def get_time_series_for_symbol(symbol, duration="6m"):
    """
    Get a time series of quotes for the given symbol.

    Arguments:
        symbol (str): the desired stock symbol
        duration (str): the length of the time series
                        (1d, 1m, 3m, 6m, ytd, 1y, 2y, 5y)
    """

    query_string = "/stock/{0}/chart/{1}".format(symbol, duration)

    response = __send_get(URL + query_string)

    return [__quote_from_json(q) for q in response.json()]

def __send_get(url):
    """
    Send a GET to the url.

    Arguments:
        url (str): the endpoint and query parameters
    """

    logging.debug("GET %s", url)

    response = requests.get(url)

    if response.status_code == 200:
        return response

    raise Exception("bad stuff")

def __quote_from_json(json):
    timestamp = datetime.strptime(json["date"], "%Y-%m-%d")
    price = float(json["close"])

    return Quote(timestamp, price)
