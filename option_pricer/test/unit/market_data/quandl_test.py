"""
Quandl API test module.
"""

from datetime import datetime

import unittest
import requests_mock

from option_pricer.market_data import quandl
from option_pricer.market_data.rate import Rate

class TestQuandl(unittest.TestCase):
    """
    Quandl test class.
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
    def test_current_rate(self, request_mock):
        """
        Test the retrieval of the most recent interest rate.
        """

        address = quandl.URL + "/datasets/USTREASURY/YIELD.json?api_key{0}".format(
            quandl.API_KEY
        )

        request_mock.get(
            address,
            status_code=200,
            json={
                "dataset": {
                    "column_names": [
                        "Date",
                        "1 MO",
                        "3 MO",
                        "6 MO",
                        "1 YR",
                        "2 YR",
                        "3 YR",
                        "5 YR",
                        "7 YR",
                        "10 YR",
                        "20 YR",
                        "30 YR"
                    ],
                    "data": [
                        [
                            "2018-03-16",
                            1.71,
                            1.78,
                            1.96,
                            2.08,
                            2.31,
                            2.44,
                            2.65,
                            2.78,
                            2.85,
                            2.96,
                            3.08
                        ],
                    ]
                },
            }
        )

        rate = quandl.get_current_rate()

        self.assertEqual(rate, Rate(datetime(2018, 3, 16), 0.0208))
