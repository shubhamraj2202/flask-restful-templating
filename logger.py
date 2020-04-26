"""
Custom Logger Class with Color and file write option
"""
import logging

class CustomFormatter(logging.Formatter):
    """
        Custom Logging Formatter to add colors and count warning / errors
    """

    grey = "\x1b[38;21m"
    cyan = "\x1b[36;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    white_red = "\x1b[41;1m"
    custom_format = "%(asctime)s (%(filename)s:%(lineno)d) [%(levelname)s]: %(message)s"

    FORMATS = {
        logging.DEBUG: grey + custom_format + reset,
        logging.INFO: cyan + custom_format + reset,
        logging.WARNING: yellow + custom_format + reset,
        logging.ERROR: red + custom_format + reset,
        logging.CRITICAL: white_red + custom_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def get_logger(namespace=__name__, level='info', log_file=None):
    """
    Create Logger, set log level, instantiate file & console handler
    """
    log_level = dict(info=logging.INFO, debug=logging.DEBUG)
    logger = logging.getLogger(namespace)
    logger.setLevel(log_level[level])

    # Initialize File Handler and Add to Logger
    if log_file:
        filehandler = logging.FileHandler(log_file)
        filehandler.setLevel(log_level[level])
        filehandler.setFormatter(CustomFormatter())
        logger.addHandler(filehandler)

    # Initialize Console Handler and Add to Logger
    consolehandler = logging.StreamHandler()
    consolehandler.setLevel(log_level[level])
    consolehandler.setFormatter(CustomFormatter())
    logger.addHandler(consolehandler)

    return logger
