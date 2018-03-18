"""
Instrument Quotes and related classes.
"""

class Quote(object):
    """
    An instantaneous quote for a financial instrument.

    Attributes:
        timestamp (datetime): the time of the price
        price (float): the price
    """

    def __init__(self, timestamp, price):
        """
        Constructor.

        Arguments:
            timestamp (datetime): the time of the price
            price (float): the price
        """
        self.timestamp = timestamp
        self.price = price

    def __eq__(self, other):
        """
        Compares another Quote with this one.

        Arguments:
            other(Quote): the other Quote with which to compare this one.

        Returns:
            bool: True if the quotes match, False if they don't.
        """

        return self.timestamp == other.timestamp and \
               self.price == other.price

class TimeSeriesQuote(object):
    """
    A quote for a financial instrument that represents a span of time.

    Attributes:
        start_time (datetime): the starting time of the time series interval
        end_time (datetime): the ending time of the time series interval
        open  (float): the starting price of the interval
        high  (float): the highest price seen during the interval
        low   (float): the lowest price seen during the interval
        close (float): the ending price of the interval
        volume  (int): the quantity traded during the time series interval
    """

    def __init__(self, start_time, end_time, open, high, low, close, volume):
        """
        Constructor.

        Arguments:
            start_time (datetime): the starting time of the time series interval
            end_time (datetime): the ending time of the time series interval
            open  (float): the starting price of the interval
            high  (float): the highest price seen during the interval
            low   (float): the lowest price seen during the interval
            close (float): the ending price of the interval
            volume  (int): the quantity traded during the time series interval
        """
        self.start_time = start_time
        self.end_time = end_time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def __eq__(self, other):
        """
        Compares another TimeSeriesQuote with this one.

        Arguments:
            other(TimeSeriesQuote): the other TimeSeriesQuote with which to compare this one.

        Returns:
            bool: True if the quotes match, False if they don't.
        """

        return self.start_time == other.start_time and \
               self.end_time == other.end_time and \
               self.open == other.open and \
               self.high == other.high and \
               self.low == other.low and \
               self.close == other.close and \
               self.volume == other.volume
