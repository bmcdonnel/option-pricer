"""
Instrument Quotes and related classes.
"""

import math

class Quote(object):
    """
    A quote for a financial instrument.

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
               math.isclose(self.price, other.price)
