"""
Instrument Rates and related classes.
"""

import math

class Rate(object):
    """
    An interest rate.

    Attributes:
        timestamp (datetime): the time when the rate was applicable
        percentage_yield (float): the percentage yield
    """

    def __init__(self, timestamp, percentage_yield):
        """
        Constructor.

        Attributes:
            timestamp (datetime): the time when the rate was applicable
            percentage_yield (float): the percentage yield
        """
        self.timestamp = timestamp
        self.percentage_yield = percentage_yield

    def __eq__(self, other):
        """
        Compares another Rate with this one.

        Arguments:
            other(Rate): the other Rate with which to compare this one.

        Returns:
            bool: True if the rates match, False if they don't.
        """

        return self.timestamp == other.timestamp and \
               math.isclose(self.percentage_yield, other.percentage_yield)
