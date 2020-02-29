import logging

from drf_logger.formatters import SimpleExtraFormatter


def get_default_logger(name: str) -> logging.Logger:
    """ Get logging.Logger instance used in testing and decorators.py.

    Args:
        name (str): The name of Logger instance used in
                    logging.getLogger(name).

    Returns:
        logging.Logger: A logger instance with level='INFO',
                        handler=logging.StreamhHandler,
                        formatter=SimpleExtraFormatter.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = SimpleExtraFormatter()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
