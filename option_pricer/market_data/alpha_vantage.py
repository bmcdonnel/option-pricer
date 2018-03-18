"""
Alpha Vantage market data implementation.
"""

import requests

API_KEY = "UGALH9VPSPD5Z0IN"
URL = "https://www.alphavantage.co/query?"

def get_quote(symbol):
    """
    Get a quote for the given symbol.

    Arguments:
    symbol (str): the desired symbol
    """

    query_string = "function={0}&symbols={1}&apikey={2}".format(
        "BATCH_STOCK_QUOTES",
        symbol,
        API_KEY,
    )

    response = requests.get(URL + query_string)

    if response.status_code != 200:
        raise Exception("bad stuff")

    return float(response.json()["Stock Quotes"][0]["2. price"])
