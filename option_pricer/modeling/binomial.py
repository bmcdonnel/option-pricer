"""
Binomial pricing model variants and related classes.
"""

import logging
from math import exp, sqrt

from option_pricer.market_data import iex
from option_pricer.market_data import quandl
from option_pricer.modeling.volatility import VolatilityCalculator

class CoxRussRubinstein(object):
    """
    Cox-Russ-Rubinstein implementation of the binomial pricing model. This variant
    is based on the principle that returns over a small time period will approximate a
    risk-free return. It also assumes that the amount the underlying might moves up is
    the inverse of the amount it might move down.
    """

    def __init__(self, steps, step_size):
        """
        Constructor.

        Arguments:
            steps (int): the number of steps for which the model should run
            step_size (float): the size of each time step
        """
        self.steps = steps
        self.step_size = step_size

    def price_contract(self, underlying, expiration, contract_type, strike):
        """
        Calculates the price for an option contract with the provided charactistics.

        Arguments:
            underlying (str): the underlying stock symbol
            expiration (datetime): the expiration date of the contract
            contract_type (str): put or call
            strike (float): the strike price of the option contract
        """

        logging.info(
            "Calculating price for %s %s %.2f %s",
            underlying,
            expiration.strftime("%Y-%m-%d"),
            strike,
            contract_type,
        )

        quotes = iex.get_time_series_for_symbol(underlying)

        logging.info("Got %i daily quotes for %s", len(quotes), underlying)

        rate = quandl.get_current_rate()

        logging.info("Current interest rate: %.6f", rate.percentage_yield)

        volatility = VolatilityCalculator(quotes).annualized_volatility

        logging.info("%s volatility: %.6f", underlying, volatility)

        up = exp(volatility * sqrt(self.step_size))
        down = 1 / up
        probability = (exp(rate.percentage_yield * self.step_size) - down) / (up - down)

        logging.info("u: %.6f, d: %.6f, p: %.6f", up, down, probability)
