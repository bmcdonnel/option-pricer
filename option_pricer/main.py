import logging
import os
import sys

from option_pricer import utils

LOG_PATH = 'logs'
"""str: The path where the log file is stored.
"""

def main():
    if len(sys.argv) > 2:
        print 'usage: python -m main.py [filename|stdin]'
        return

    utils.configure_rolling_logger(os.path.join(LOG_PATH, 'application.log'))

if __name__ == "__main__":
    main()
