"""
Volatility calculations and related classes.
"""

from statistics import stdev

import math

TRADING_DAYS_PER_YEAR = 252
"""
The number of trading days in a single year in the United States.
"""

class VolatilityCalculator(object):
    """
    This class calculates the volatilty of an instrument given a set of price quotes.

    Attributes:
        quotes (array): the price quotes used for determining the volatility
        volatility (float): the calculated volatility
        annualized_volatility (float): the calcalated volatility as an annualized value
    """

    def __init__(self, quotes):
        self.quotes = quotes
        self.volatility = self._calculate_volatility()
        self.annualized_volatility = math.sqrt(TRADING_DAYS_PER_YEAR) * self.volatility

    def _calculate_volatility(self):
        daily_returns = []

        previous_price = self.quotes[0].price
        for quote in self.quotes[1:]:
            price = quote.price
            percentage_change = (price / previous_price) - 1

            daily_returns.append(percentage_change)
            previous_price = price

        return stdev(daily_returns)
