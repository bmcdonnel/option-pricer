"""This module contains some utilty functions.
"""

import logging
import logging.handlers
import os

def configure_rolling_logger(log_filename):
    """Configures a midnight rolling log file with the provided file name.

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

