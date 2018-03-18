"""
Alpha Vantage market data test module.
"""

import unittest
import requests_mock

from option_pricer.market_data import alpha_vantage

class TestAlphaVantage(unittest.TestCase):
    """
    Alpha Vantage test class.
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

    @requests_mock.mock()
    def test_get_quote_successful(self, request_mock):
        """
        Test the get_quote() functionality.
        """
        request_mock.get(
            alpha_vantage.URL + "function={0}&symbols={1}&apikey={2}".format(
                "BATCH_STOCK_QUOTES",
                "TSLA",
                alpha_vantage.API_KEY,
            ),
            status_code=200,
            json={
                "Stock Quotes": [
                    {"2. price" : "100.00"},
                ]
            }
        )

        self.assertEqual(alpha_vantage.get_quote("TSLA"), 100.0)
