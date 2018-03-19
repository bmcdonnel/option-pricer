"""
Alpha Vantage market data implementation.
"""

from datetime import datetime, timedelta
from enum import Enum

import logging
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
        """
        Converts an IntradayQuoteInterval into a datetime.timedelta.
        """
        return {
            IntradayQuoteInterval.ONE_MINUTE:      timedelta(minutes=1),
            IntradayQuoteInterval.FIVE_MINUTES:    timedelta(minutes=5),
            IntradayQuoteInterval.FIFTEEN_MINUTES: timedelta(minutes=15),
            IntradayQuoteInterval.THIRTY_MINUTES:  timedelta(minutes=30),
            IntradayQuoteInterval.SIXTY_MINUTES:   timedelta(minutes=60),
        }.get(self)

class TimeSeriesOutputSize(Enum):
    """
    An enumeration of time series output sizes for use with daily, weekly, and monthly
    time series calls.

    COMPACT: 100 data points
    FULL: as many data points as available
    """

    COMPACT = "compact"
    FULL = "full"

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

    query_string = "function={0}&symbol={1}&interval={2}&apikey={3}".format(
        "TIME_SERIES_INTRADAY",
        symbol,
        interval.value,
        API_KEY,
    )

    response = _send_get(query_string)

    key = "Time Series ({0})".format(interval.value)
    series = response.json()[key]
    duration = interval.duration()
    transform = lambda k: datetime.strptime(k, "%Y-%m-%d %H:%M:%S")

    return [_time_series_quote_from_json(transform(k), v, duration) for k, v in series.items()]

def get_daily_time_series(symbol, output_size=TimeSeriesOutputSize.COMPACT):
    """
    For the given symbol, get a time series of prices for the current (or
    most recent) trading day with the specified output size.

    Arguments:
        symbol (str): the desired symbol
        output_size (TimeSeriesOutputSize): the desired output size for the time series
    """

    if not isinstance(output_size, TimeSeriesOutputSize):
        raise ValueError(
            "output_size '{0}' is not a valid TimeSeriesOutputSize".format(
                output_size
            )
        )

    query_string = "function={0}&symbol={1}&outputsize={2}&apikey={3}".format(
        "TIME_SERIES_DAILY",
        symbol,
        output_size.value,
        API_KEY,
    )

    response = _send_get(query_string)

    series = response.json()["Time Series (Daily)"]
    duration = timedelta(hours=24)
    transform = lambda k: datetime.strptime(k, "%Y-%m-%d")

    return [_time_series_quote_from_json(transform(k), v, duration) for k, v in series.items()]

def _send_get(query_string):
    """
    Send a GET to Alpha Vantage.

    Arguments:
        query_string (str): the endpoint and query parameters
    """

    logging.debug(URL + query_string)

    response = requests.get(URL + query_string)

    if response.status_code == 200 and "Error Message" not in response.json().keys():
        return response

    raise Exception("bad stuff")

def _quote_from_json(json):
    timestamp = datetime.strptime(json["4. timestamp"], "%Y-%m-%d %H:%M:%S")
    price = float(json["2. price"])

    return Quote(timestamp, price)

def _time_series_quote_from_json(timestamp, json, duration):
    open_price = float(json["1. open"])
    high_price = float(json["2. high"])
    low_price = float(json["3. low"])
    close_price = float(json["4. close"])
    volume = float(json["5. volume"])

    return TimeSeriesQuote(
        timestamp,
        timestamp + duration,
        open_price,
        high_price,
        low_price,
        close_price,
        volume
    )
