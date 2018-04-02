"""
Market Data module using IEX Trading's free API.
"""

from datetime import datetime

from option_pricer.market_data.quote import Quote
from option_pricer.utils import send_get

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

    response = send_get(URL + query_string)

    def quote_from_json(json):
        """
        Builds a Quote object from JSON.
        """
        timestamp = datetime.strptime(json["date"], "%Y-%m-%d")
        price = float(json["close"])

        return Quote(timestamp, price)

    return [quote_from_json(q) for q in response.json()]

def get_quote_for_symbol(symbol):
    """
    Get a quote for the given symbol.

    Arguments:
        symbol (str): the desired stock symbol
    """

    query_string = "/stock/{0}/quote".format(symbol)

    response = send_get(URL + query_string)

    def quote_from_json(json):
        """
        Builds a Quote object from JSON.
        """
        timestamp = datetime.fromtimestamp(float(json["latestUpdate"])/1000)
        price = float(json["latestPrice"])

        return Quote(timestamp, price)

    return quote_from_json(response.json())
