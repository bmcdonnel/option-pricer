"""
Volatility calculations and related classes.
"""

from enum import Enum
from statistics import stdev

import math

TRADING_DAYS_PER_YEAR = 252
"""
The number of trading days in a single year in the United States.
"""

class PriceSelectionMethod(Enum):
    """
    An enumeration of possible methods for selecting a price from a quote.
    """

    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    AVERAGE = "average"

class VolatilityCalculator(object):
    """
    This class calculates the volatilty of an instrument given a set of price quotes.

    Attributes:
        quotes (array): the price quotes used for determining the volatility
        volatility (float): the calculated volatility
        annualized_volatility (float): the calcalated volatility as an annualized value
    """

    __PRICE_TRANSFORMER = {
        PriceSelectionMethod.OPEN: lambda q: q.open,
        PriceSelectionMethod.HIGH: lambda q: q.high,
        PriceSelectionMethod.LOW: lambda q: q.low,
        PriceSelectionMethod.CLOSE: lambda q: q.close,
        PriceSelectionMethod.AVERAGE: lambda q: (q.high + q.low) / 2,
    }

    def __init__(self, quotes, price_selection_method=PriceSelectionMethod.CLOSE):
        self.quotes = quotes
        self.price_selection_method = price_selection_method
        self.volatility = self._calculate_volatility()
        self.annualized_volatility = math.sqrt(TRADING_DAYS_PER_YEAR) * self.volatility

    def _get_price(self, quote):
        return self.__PRICE_TRANSFORMER.get(self.price_selection_method)(quote)

    def _calculate_volatility(self):
        daily_returns = []

        previous_price = self._get_price(self.quotes[0])
        for quote in self.quotes[1:]:
            price = self._get_price(quote)
            percentage_change = (price / previous_price) - 1

            daily_returns.append(percentage_change)
            previous_price = price

        return stdev(daily_returns)
