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

        initialize_tree(tree, 2, 0.50, 10)

        self.assertEqual(
            tree,
            [
                [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [20, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [40, 10, 2.5, 0, 0, 0, 0, 0, 0, 0, 0],
                [80, 20, 5, 1.25, 0, 0, 0, 0, 0, 0, 0],
                [160, 40, 10, 2.5, 0.625, 0, 0, 0, 0, 0, 0],
                [320, 80, 20, 5, 1.25, 0.3125, 0, 0, 0, 0, 0],
                [640, 160, 40, 10, 2.5, 0.625, 0.15625, 0, 0, 0, 0],
                [1280, 320, 80, 20, 5, 1.25, 0.3125, 0.078125, 0, 0, 0],
                [2560, 640, 160, 40, 10, 2.5, 0.625, 0.15625, 0.0390625, 0, 0],
                [5120, 1280, 320, 80, 20, 5, 1.25, 0.3125, 0.078125, 0.01953125, 0],
                [10240, 2560, 640, 160, 40, 10, 2.5, 0.625, 0.15625, 0.0390625, 0.009765625],
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

        contract_price = calculate_contract_price(tree, "C", contract_strike_price, p, 0.05, 0.01)

        self.assertEqual(round(contract_price, 6), 1.627916)
