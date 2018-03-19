"""
Volatility test module.
"""

from datetime import datetime

import unittest
import math

from option_pricer.modeling.volatility import VolatilityCalculator, PriceSelectionMethod
from option_pricer.market_data.quote import TimeSeriesQuote

class TestVolatilityCalculator(unittest.TestCase):
    """
    VolatilityCalculator test class.
    """

    def setUp(self):
        """
        Test setup logic.
        """
        pass

    def tearDown(self):
        """
        Test tear down logic.
        """
        pass

    def test_volatility_calculator(self):
        """
        Test the VolatilityCalculator using PriceSelectionMethod.OPEN prices.
        """
        quotes = [
            TimeSeriesQuote(datetime.now(), datetime.now(), 147.82, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 149.5, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 149.78, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 149.86, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 149.93, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 150.89, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 152.39, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 153.74, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 152.79, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 151.23, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 151.78, 0, 0, 0, 0),
        ]

        calculator = VolatilityCalculator(quotes, PriceSelectionMethod.OPEN)

        self.assertTrue(math.isclose(calculator.volatility, 0.0069594213778736355))
        self.assertTrue(math.isclose(calculator.annualized_volatility, 0.11047738940856067))
