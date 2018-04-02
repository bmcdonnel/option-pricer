"""
Binomial test module.
"""

from datetime import datetime, timedelta

import unittest

from option_pricer.modeling.binomial import initialize_tree
from option_pricer.modeling.binomial import calculate_contract_price
from option_pricer.modeling.binomial import calculate_time_step_duration

class TestVolatilityCalculator(unittest.TestCase):
    """
    VolatilityCalculator test class.
    """

    def test_tree_init(self):
        """
        Test binomial tree initialization.
        """

        tree = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        initialize_tree(tree, 1, 1, 100)

        self.assertEqual(
            tree,
            [
                [100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [101, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [102, 100, 98, 0, 0, 0, 0, 0, 0, 0, 0],
                [103, 101, 99, 97, 0, 0, 0, 0, 0, 0, 0],
                [104, 102, 100, 98, 96, 0, 0, 0, 0, 0, 0],
                [105, 103, 101, 99, 97, 95, 0, 0, 0, 0, 0],
                [106, 104, 102, 100, 98, 96, 94, 0, 0, 0, 0],
                [107, 105, 103, 101, 99, 97, 95, 93, 0, 0, 0],
                [108, 106, 104, 102, 100, 98, 96, 94, 92, 0, 0],
                [109, 107, 105, 103, 101, 99, 97, 95, 93, 91, 0],
                [110, 108, 106, 104, 102, 100, 98, 96, 94, 92, 90],
            ]
        )

    def test_calc_time_step_duration(self):
        """
        Test time step duration calculation.
        """

        self.assertEqual(
            calculate_time_step_duration(timedelta(days=252), 252),
            1.0/252.0
        )

    def test_calculate_contract_price(self):
        """
        Test time step duration calculation.
        """

        steps = 100
        u = 1.0202013400267558
        d = 0.9801986733067554
        p = 0.5075024586780919

        tree = [[0 for x in range(steps + 1)] for y in range(steps + 1)]

        current_underlying_price = 50
        contract_strike_price = 60

        initialize_tree(tree, u, d, current_underlying_price)

        """
        self.assertEqual(
            calculate_contract_price(tree, "C", contract_strike_price, p, 0.05, 0.01),
            1.628
        )
        """

    def test_simple_contract_calc(self):

        """
        Test time step duration calculation.
        """

        steps = 5

        u = 1.0512710963760241
        d = 0.9512294245007139
        p = 0.49250177047752547

        tree = [[0 for x in range(steps + 1)] for y in range(steps + 1)]

        current_underlying_price = 50
        contract_strike_price = 51

        initialize_tree(tree, u, d, current_underlying_price)

        """
        self.assertEqual(
            calculate_contract_price(tree, "C", contract_strike_price, p, 0.05, 0.01),
            1.628
        )
        """
