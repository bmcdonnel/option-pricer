"""
Volatility test module.
"""

from datetime import datetime, timedelta

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
            TimeSeriesQuote(datetime.now(), datetime.now(), 1.5, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 2.5, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 2.5, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 2.75, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 3.25, 0, 0, 0, 0),
            TimeSeriesQuote(datetime.now(), datetime.now(), 4.75, 0, 0, 0, 0),
        ]

        calculator = VolatilityCalculator(quotes, PriceSelectionMethod.OPEN)

        self.assertTrue(math.isclose(calculator.volatility, 1.0810874155219827))
