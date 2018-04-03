"""
Binomial pricing model variants and related classes.
"""

import logging
from datetime import datetime, timedelta
from math import exp, sqrt

from option_pricer.market_data import iex
from option_pricer.market_data import quandl
from option_pricer.modeling.volatility import VolatilityCalculator, TRADING_DAYS_PER_YEAR

def calculate_time_step_duration(time_to_expiration, steps):
    """
    Calculate the time step duration given the time to expiration and the
    number of steps in the tree.

    Arguments:
        time_to_expiration (timedelta): the length of time until the
            contract expires
        steps (int): the number of steps in tree
    """
    return time_to_expiration / timedelta(days=TRADING_DAYS_PER_YEAR) / steps

def calculate_volatility(underlying):
    """
    Calculates the volatility of the underlying.

    Arguments:
        underlying (str): the underlying symbol
    """

    quotes = iex.get_time_series_for_symbol(underlying)

    logging.info("Got %i daily quotes", len(quotes))

    volatility = VolatilityCalculator(quotes).annualized_volatility

    return volatility

def initialize_tree(price_tree, up, down, current_price):
    """
    Initializes a binomial pricing tree with price values.

    Arguments:
        price_tree (list): 2 dimensional array/list
        up (float): the dollar amount that the underlying will move up each step
        down (float): the dollar amount that the underlying will move down each step
        current_price (float): the current price of the underlying from which the
            binomial tree will start
    """

    size = len(price_tree)

    price_tree[0][0] = current_price

    for i in range(1, size):
        for j in range(i + 1):
            price_tree[i][j] = current_price * pow(up, i - j) * pow(down, j)

def calculate_contract_price(
        price_tree,
        contract_type,
        strike,
        probability,
        percentage_yield,
        time_step_duration,
        exercise_early=True):
    """
    Calculate the price of an option contract with the specified characteristics.

    Arguments:
        price_tree (list): an initialized 2 dimension array
        contract_type (str): "P" for put, "C" for call
        strike (float): the strike price of the option contract
        probability (float): the probability the stock price will move in one direction
        percentage_yield (float): annualized risk free rate with value
            in the interval [0.0, 1.0]
        time_step_duration (float): time duration of a single time step in the model expressed
            as a fraction of a year
    """

    for j in range(len(price_tree[-1])):
        if contract_type == "P":
            price_tree[-1][j] = max(strike - price_tree[-1][j], 0)
        else:
            price_tree[-1][j] = max(price_tree[-1][j] - strike, 0)

    size = len(price_tree)

    for i in range(size - 2, -1, -1):
        for j in range(i + 1):
            prob_up = probability * price_tree[i + 1][j]
            prob_down = (1 - probability) * price_tree[i + 1][j + 1]

            option_price = exp(-percentage_yield * time_step_duration) * (prob_up + prob_down)

            if exercise_early:
                if contract_type == "P":
                    price_tree[i][j] = max(strike - price_tree[i][j], option_price)
                else:
                    price_tree[i][j] = max(price_tree[i][j] - strike, option_price)
            else:
                price_tree[i][j] = option_price

    return price_tree[0][0]

class CoxRussRubinstein(object):
    """
    Cox-Russ-Rubinstein implementation of the binomial pricing model. This variant
    is based on the principle that returns over a small time period will approximate a
    risk-free return. It also assumes that the amount the underlying might moves up is
    the inverse of the amount it might move down.
    """

    def __init__(self, steps):
        """
        Constructor.

        Arguments:
            steps (int): the number of steps for which the model should run
        """
        self.steps = steps
        self.price_tree = [[0 for x in range(self.steps + 1)] for y in range(self.steps + 1)]

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

        volatility = calculate_volatility(underlying)

        logging.info("%s volatility: %.6f", underlying, volatility)

        rate = quandl.get_current_rate()

        logging.info("Current interest rate: %.6f per year", rate.percentage_yield)

        time_to_expiration = expiration - datetime.now()

        logging.info("Days to expiration: %d", time_to_expiration.days)

        time_step_duration = calculate_time_step_duration(time_to_expiration, self.steps)

        logging.info("Time steps: %d, %.6f years/step", self.steps, time_step_duration)

        up, down, probability = CoxRussRubinstein.calculate_inputs(
            volatility,
            rate.percentage_yield,
            time_step_duration
        )

        logging.info("Model inputs: u: %.6f, d: %.6f, p: %.6f", up, down, probability)

        quote = iex.get_quote_for_symbol(underlying)

        logging.info("Underlying price: $%.6f", quote.price)

        initialize_tree(self.price_tree, up, down, quote.price)

        contract_price = calculate_contract_price(
            self.price_tree,
            contract_type,
            strike,
            probability,
            rate.percentage_yield,
            time_step_duration,
        )

        logging.info("Contract price: $%.6f", contract_price)

        return contract_price

    @staticmethod
    def calculate_inputs(volatility, percentage_yield, time_step_duration):
        """
        Calculates the 3 inputs to the binomial pricing model: u, d, and p.

        Arguments:
            volatility (float): annualized volatility for the underlying
            percentage_yield (float): annualized risk free rate with value
                                      in the interval [0.0, 1.0]
            time_step_duration (float): time duration of a single time step in the model expressed
                                        as a fraction of a year
        """

        up = exp(volatility * sqrt(time_step_duration))
        down = 1 / up
        probability = (exp(percentage_yield * time_step_duration) - down) / (up - down)

        return up, down, probability
