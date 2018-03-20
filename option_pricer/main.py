"""
This module is a option contract pricer.

Attributes:
    LOG_PATH (str): the directory to which the log file will be written.
"""

import argparse
import os
from datetime import datetime

import option_pricer.modeling.binomial as binomial
from option_pricer import utils

LOG_PATH = "logs"
"""
str: The path where the log file is stored.
"""

BINOMIAL_VARIANTS = ["CRR"]
"""
list: Currently supported binomial pricing model variants
"""

def valid_date(date_string):
    """
    Validate date input.

    Arguments:
    date_string (str): the input string
    """

    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        message = "Invalid date string: '{0}'".format(date_string)
        raise argparse.ArgumentTypeError(message)

def valid_type(type_string):
    """
    Validate option type input.

    Arguments:
    type_string (str): the input string
    """

    if type_string.upper() in ["P", "C"]:
        return type_string.upper()
    else:
        message = "Invalid type string: '{0}'".format(type_string)
        raise argparse.ArgumentTypeError(message)

def valid_variant(variant_string):
    """
    Validate binomial pricing model variant input.

    Arguments:
    variant_string (str): the input string
    """

    if variant_string.upper() in BINOMIAL_VARIANTS:
        return variant_string.upper()
    else:
        message = "Invalid variant string: '{0}'".format(variant_string)
        raise argparse.ArgumentTypeError(message)

def parse_arguments():
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "--underlying",
        required=True,
        type=str,
        help="The option contract's underlying symbol"
    )

    parser.add_argument(
        "--expiration",
        required=True,
        type=valid_date,
        help="The expiration date of the option contract: YYYY-MM-DD"
    )

    parser.add_argument(
        "--type",
        required=True,
        type=valid_type,
        help="The option contract type: P or C"
    )

    parser.add_argument(
        "--strike",
        required=True,
        type=float,
        help="The option contract strike price"
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=100,
        help="The number of time steps to calculate"
    )

    parser.add_argument(
        "--size",
        type=float,
        default=0.01,
        help="The size of the time steps"
    )

    parser.add_argument(
        "--variant",
        type=valid_variant,
        default="crr",
        help="The binomial model variant to use: {0}".format(BINOMIAL_VARIANTS)
    )

    return parser.parse_args()

def main():
    """
    This is the main function.
    """

    args = parse_arguments()

    utils.configure_rolling_logger(os.path.join(LOG_PATH, "application.log"))

    model_class = {
        "CRR": binomial.CoxRussRubinstein,
    }.get(args.variant)

    model = model_class(
        args.steps,
        args.size,
    )

    model.price_contract(
        args.underlying,
        args.expiration,
        args.type,
        args.strike,
    )

if __name__ == "__main__":
    main()
