"""
Interest rate module using Quandl's free API.
"""

from datetime import datetime

from option_pricer.market_data.rate import Rate
from option_pricer.utils import send_get

API_KEY = "iz6oLgxG7psZjes661z8"
URL = "https://www.quandl.com/api/v3"

def get_current_rate(duration="1 YR"):
    """
    Get the most recent rate for the duration yield desired.

    Arguments:
        duration (str): the deposit duration for the desired rate
                        ("1 MO", "3 MO", "6 MO", "1 YR", "2 YR", "3 YR")
    """

    query_string = "/datasets/USTREASURY/YIELD.json?api_key={0}".format(API_KEY)

    response = send_get(URL + query_string)

    return __rate_from_json(response.json(), duration)

def __rate_from_json(json, duration):
    column_names = json["dataset"]["column_names"]
    desired_column = [idx for idx, val in enumerate(column_names) if val == duration][0]

    item = json["dataset"]["data"][0]

    return Rate(
        datetime.strptime(item[0], "%Y-%m-%d"),
        float(item[desired_column]) / 100.0
    )
