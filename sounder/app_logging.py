"""
Sound analyser logging.
"""

import logging
import logging.config
import logging.handlers
import time

DEFAULT_LOG_LEVEL = 20

def setup_logging(name: str) -> None:
    """
    Sets up the logging handle.

    Args:
        name:   Name for logger
    """

    # Create logger.
    log = logging.getLogger(name)
    # Use default logging level.
    log.setLevel(DEFAULT_LOG_LEVEL)
    # Setup log handler for rotating files.
    handler = logging.handlers.RotatingFileHandler(name + '.log')
    handler.setFormatter(logging.Formatter(fmt='%(asctime)s.%(msecs)03d [%(name)s] [%(levelname)-8s] %(message)s', datefmt='%Y%m%d-%H:%M:%S', style='%'))
    logging.Formatter.converter = time.localtime
    # Add log handler to logger.
    log.addHandler(handler)
