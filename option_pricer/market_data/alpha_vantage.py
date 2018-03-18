"""
Alpha Vantage market data implementation.
"""

from datetime import datetime, timedelta
from enum import Enum

import requests

from option_pricer.market_data.quote import Quote, TimeSeriesQuote

API_KEY = "UGALH9VPSPD5Z0IN"
URL = "https://www.alphavantage.co/query?"

class IntradayQuoteInterval(Enum):
    """
    An enumeration of valid intraday time series intervals.
    """

    ONE_MINUTE = "1min"
    FIVE_MINUTES = "5min"
    FIFTEEN_MINUTES = "15min"
    THIRTY_MINUTES = "30min"
    SIXTY_MINUTES = "60min"

    def duration(self):
        return {
            IntradayQuoteInterval.ONE_MINUTE:      timedelta(minutes=1),
            IntradayQuoteInterval.FIVE_MINUTES:    timedelta(minutes=5),
            IntradayQuoteInterval.FIFTEEN_MINUTES: timedelta(minutes=15),
            IntradayQuoteInterval.THIRTY_MINUTES:  timedelta(minutes=30),
            IntradayQuoteInterval.SIXTY_MINUTES:   timedelta(minutes=60),
        }.get(self)

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

    response = _send_get(query_string)

    return _quote_from_json(response.json()["Stock Quotes"][0])

def get_intraday_time_series(symbol, interval):
    """
    For the given symbol, get a time series of prices for the current (or
    most recent) trading day with the specified time interval between quotes.

    Arguments:
        symbol (str): the desired symbol
        interval (IntradayQuoteInterval): the desired interval between quotes
    """

    if not isinstance(interval, IntradayQuoteInterval):
        raise ValueError(
            "interval '{0}' is not a valid IntradayQuoteInterval".format(
                interval
            )
        )

    query_string = "function={0}&symbols={1}&interval={2}&apikey={3}".format(
        "TIME_SERIES_INTRADAY",
        symbol,
        interval.value,
        API_KEY,
    )

    response = _send_get(query_string)

    key = "Time Series ({0})".format(interval.value)
    series = response.json()[key]

    return [_time_series_quote_from_json(k, v, interval) for k, v in series.items()]

def _send_get(query_string):
    """
    Send a GET to Alpha Vantage.

    Arguments:
        query_string (str): the endpoint and query parameters
    """

    response = requests.get(URL + query_string)

    if response.status_code != 200:
        raise Exception("bad stuff")

    return response

def _quote_from_json(json):
    timestamp = datetime.strptime(json["4. timestamp"], "%Y-%m-%d %H:%M:%S")
    price = float(json["2. price"])

    return Quote(timestamp, price)

def _time_series_quote_from_json(timestamp, json, interval):
    timestamp   = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    open_price  = float(json["1. open:"])
    high_price  = float(json["2. high:"])
    low_price   = float(json["3. low:"])
    close_price = float(json["4. close:"])
    volume      = float(json["5. volume:"])

    return TimeSeriesQuote(
        timestamp,
        timestamp + interval.duration(),
        open_price,
        high_price,
        low_price,
        close_price,
        volume
    )
