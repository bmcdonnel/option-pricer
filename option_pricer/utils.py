"""
This module contains some utilty functions.  """

import logging
import logging.handlers
import os
import requests

def configure_rolling_logger(log_filename):
    """
    Configures a midnight rolling log file with the provided file name.

    Args:
        log_filename (str): an absolute path file name

    Returns:
        logger: the root logger that was configured
    """

    file_path, _ = os.path.split(log_filename)

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    # root logger
    logger = logging.getLogger('')

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.handlers.TimedRotatingFileHandler(log_filename, 'midnight')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

def send_get(url):
    """
    Send a GET to the url.

    Arguments:
        url (str): the endpoint and query parameters
    """

    logging.debug("GET %s", url)

    response = requests.get(url)

    if response.status_code == 200:
        return response

    raise Exception("bad stuff")

def print_tree(tree):
    for i in range(len(tree)):
        print_array(tree[i])

def print_array(array):
    print("".join("%.4f, " % (k) for k in array))
