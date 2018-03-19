"""
Alpha Vantage market data test module.
"""

from datetime import datetime, timedelta

import unittest
import requests_mock

from option_pricer.market_data import alpha_vantage
from option_pricer.market_data.quote import Quote, TimeSeriesQuote

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
        Test get_quote() functionality when the request is successful.
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
                    {
                        "2. price" : "100.00",
                        "4. timestamp" : "2018-03-16 15:59:59"
                    },
                ]
            }
        )

        self.assertEqual(
            alpha_vantage.get_quote("TSLA"),
            Quote(datetime(2018, 3, 16, 15, 59, 59), 100.0)
        )

    @requests_mock.mock()
    def test_get_quote_failure(self, request_mock):
        """
        Test get_quote() functionality when the request fails.
        """

        request_mock.get(
            alpha_vantage.URL + "function={0}&symbols={1}&apikey={2}".format(
                "BATCH_STOCK_QUOTES",
                "TSLA",
                alpha_vantage.API_KEY,
            ),
            status_code=500,
        )

        with self.assertRaises(Exception):
            alpha_vantage.get_quote("TSLA")

    @requests_mock.mock()
    def test_get_intraday_time_series(self, request_mock):
        """
        Test get_intraday_time_series() when the request is successful.
        """

        request_mock.get(
            alpha_vantage.URL + "function={0}&symbol={1}&interval={2}&apikey={3}".format(
                "TIME_SERIES_INTRADAY",
                "MSFT",
                "1min",
                alpha_vantage.API_KEY,
            ),
            status_code=200,
            json={
                "Time Series (1min)": {
                    "2018-03-16 15:54:00" : {
                        "1. open"   : "94.5000",
                        "2. high"   : "94.5600",
                        "3. low"    : "94.4500",
                        "4. close"  : "94.5000",
                        "5. volume" : "221592",
                    },
                    "2018-03-16 15:53:00" : {
                        "1. open"   : "94.5000",
                        "2. high"   : "94.6200",
                        "3. low"    : "94.5000",
                        "4. close"  : "94.6101",
                        "5. volume" : "324491",
                    },
                }
            }
        )

        time_series = alpha_vantage.get_intraday_time_series(
            "MSFT",
            alpha_vantage.IntradayQuoteInterval.ONE_MINUTE
        )

        dt1 = datetime(2018, 3, 16, 15, 54, 00)
        dt2 = datetime(2018, 3, 16, 15, 53, 00)

        self.assertEqual(
            time_series,
            [
                TimeSeriesQuote(
                    dt1,
                    dt1 + timedelta(minutes=1),
                    94.5, 94.56, 94.45, 94.5, 221592
                ),
                TimeSeriesQuote(
                    dt2,
                    dt2 + timedelta(minutes=1),
                    94.5, 94.62, 94.5, 94.6101, 324491
                ),
            ]
        )

    @requests_mock.mock()
    def test_get_daily_valid(self, request_mock):
        """
        Test get_daily_time_series() when the request is successful.
        """

        request_mock.get(
            alpha_vantage.URL + "function={0}&symbol={1}&outputsize={2}&apikey={3}".format(
                "TIME_SERIES_DAILY",
                "MSFT",
                "compact",
                alpha_vantage.API_KEY,
            ),
            status_code=200,
            json={
                "Time Series (Daily)": {
                    "2018-03-16" : {
                        "1. open"   : "94.6800",
                        "2. high"   : "95.3800",
                        "3. low"    : "93.9200",
                        "4. close"  : "94.6000",
                        "5. volume" : "47329521",
                    },
                    "2018-03-15" : {
                        "1. open"   : "93.5300",
                        "2. high"   : "94.5800",
                        "3. low"    : "92.8300",
                        "4. close"  : "94.1800",
                        "5. volume" : "26279014",
                    },
                }
            }
        )

        time_series = alpha_vantage.get_daily_time_series(
            "MSFT",
            alpha_vantage.TimeSeriesOutputSize.COMPACT
        )

        dt1 = datetime(2018, 3, 16)
        dt2 = datetime(2018, 3, 15)

        self.assertEqual(
            time_series,
            [
                TimeSeriesQuote(
                    dt1,
                    dt1 + timedelta(hours=24),
                    94.68, 95.38, 93.92, 94.6, 47329521
                ),
                TimeSeriesQuote(
                    dt2,
                    dt2 + timedelta(hours=24),
                    93.53, 94.58, 92.83, 94.18, 26279014
                ),
            ]
        )

    @requests_mock.mock()
    def test_daily_invalid(self, request_mock):
        """
        Test get_daily_time_series() when the request is invalid.
        """

        request_mock.get(
            alpha_vantage.URL + "function={0}&symbol={1}&outputsize={2}&apikey={3}".format(
                "TIME_SERIES_DAILY",
                "MSFT",
                "compact",
                alpha_vantage.API_KEY,
            ),
            status_code=200,
            json={
                "Error Message": "Invalid API call."
            }
        )

        with self.assertRaises(Exception):
            alpha_vantage.get_daily_time_series(
                "MSFT",
                alpha_vantage.TimeSeriesOutputSize.COMPACT
            )
