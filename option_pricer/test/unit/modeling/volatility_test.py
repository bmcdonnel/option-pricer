"""
Volatility test module.
"""

from datetime import datetime

import unittest
import math

from option_pricer.modeling.volatility import VolatilityCalculator
from option_pricer.market_data.quote import Quote

class TestVolatilityCalculator(unittest.TestCase):
    """
    VolatilityCalculator test class.
    """

    def test_volatility_calculator(self):
        """
        Test the VolatilityCalculator using PriceSelectionMethod.OPEN prices.
        """
        quotes = [
            Quote(datetime.now(), 147.82),
            Quote(datetime.now(), 149.50),
            Quote(datetime.now(), 149.78),
            Quote(datetime.now(), 149.86),
            Quote(datetime.now(), 149.93),
            Quote(datetime.now(), 150.89),
            Quote(datetime.now(), 152.39),
            Quote(datetime.now(), 153.74),
            Quote(datetime.now(), 152.79),
            Quote(datetime.now(), 151.23),
            Quote(datetime.now(), 151.78),
        ]

        calculator = VolatilityCalculator(quotes)

        self.assertTrue(math.isclose(calculator.volatility, 0.0069594213778736355))
        self.assertTrue(math.isclose(calculator.annualized_volatility, 0.11047738940856067))
