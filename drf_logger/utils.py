import logging

from drf_logger.formatters import JSONExtraFormatter, SimpleExtraFormatter


def get_default_logger(name: str, format_: str = 'json') -> logging.Logger:
    """ Get logging.Logger instance used in testing and decorators.py.

    Args:
        name (str): The name of Logger instance used in
                    logging.getLogger(name).
        format (str): What formatter you want to use.

    Returns:
        logging.Logger: A logger instance with level='INFO',
                        handler=logging.StreamhHandler,
                        formatter=SimpleExtraFormatter.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter: logging.Formatter
    if format_ == 'json':
        formatter = JSONExtraFormatter()
    else:
        formatter = SimpleExtraFormatter()

    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
