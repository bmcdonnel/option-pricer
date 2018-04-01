"""
IEX market data test module.
"""

from datetime import datetime

import unittest
import requests_mock

from option_pricer.market_data import iex
from option_pricer.market_data.quote import Quote

class TestIEX(unittest.TestCase):
    """
    IEX test class.
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
    def test_time_series_success(self, request_mock):
        """
        Test get_time_series_for_symbol() when the request is successful.
        """

        request_mock.get(
            iex.URL + "/stock/{0}/chart/{1}".format("AAPL", "6m"),
            status_code=200,
            json=[
                {
                    "date": "2017-12-19",
                    "open": 174.3192,
                    "high": 174.6777,
                    "low": 173.383,
                    "close": 173.8312,
                    "volume": 27436447,
                    "unadjustedVolume": 27436447,
                    "change": -1.8724,
                    "changePercent": -1.066,
                    "vwap": 173.8969,
                    "label": "Dec 19, 17",
                    "changeOverTime": 0,
                },
                {
                    "date": "2017-12-20",
                    "open": 174.1599,
                    "high": 174.7076,
                    "low": 172.5464,
                    "close": 173.642,
                    "volume": 23475649,
                    "unadjustedVolume": 23475649,
                    "change": -0.189228,
                    "changePercent": -0.109,
                    "vwap": 173.5287,
                    "label": "Dec 20, 17",
                    "changeOverTime": -0.0010884122067845105,
                },
            ]
        )

        time_series = iex.get_time_series_for_symbol("AAPL", "6m")

        self.assertEqual(
            time_series,
            [
                Quote(datetime(2017, 12, 19), 173.8312),
                Quote(datetime(2017, 12, 20), 173.642),
            ]
        )

    @requests_mock.mock()
    def test_time_series_failure(self, request_mock):
        """
        Test get_time_series_for_symbol() when the request fails.
        """

        request_mock.get(
            iex.URL + "/stock/{0}/chart/{1}".format("AAPL", "6m"),
            status_code=403,
        )

        with self.assertRaises(Exception):
            iex.get_time_series_for_symbol("AAPL", "6m")

    @requests_mock.mock()
    def test_time_series_failure(self, request_mock):
        """
        Test get_time_series_for_symbol() when the request fails.
        """

        request_mock.get(
            iex.URL + "/stock/{0}/quote".format("AAPL"),
            status_code=200,
            json={
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "primaryExchange": "Nasdaq Global Select",
                "sector": "Technology",
                "calculationPrice": "close",
                "open": 168.07,
                "openTime": 1522330200563,
                "close": 167.78,
                "closeTime": 1522353600555,
                "high": 171.75,
                "low": 166.9,
                "latestPrice": 167.78,
                "latestSource": "Close",
                "latestTime": "March 29, 2018",
                "latestUpdate": 1522353600555,
                "latestVolume": 38249433,
                "delayedPrice": 168.18,
                "delayedPriceTime": 1522357186266,
                "previousClose": 166.48,
                "change": 1.3,
                "changePercent": 0.00781,
                "avgTotalVolume": 35204320,
                "marketCap": 851317901140,
                "peRatio": 17.24,
                "week52High": 183.5,
                "week52Low": 140.06,
                "ytdChange": -0.022035958160532228
            }
        )

        quote = iex.get_quote_for_symbol("AAPL")

        self.assertEqual(quote, Quote(datetime.fromtimestamp(1522353600555.0/1000), 167.78))
