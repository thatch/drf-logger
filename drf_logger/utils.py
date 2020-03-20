import logging
from typing import Any, Callable, Tuple

from django.http import HttpRequest
from rest_framework.request import Request

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


def get_logging_function(logger: logging.Logger, level: str) -> Callable:
    """ Receive logging.Logger and logging level as args and return logging
        function which has specified level.

    Args:
        logger (logging.Logger): A logger instance to output log.
        level (str): Logging level 'DEBUG', 'INFO', 'WARNING', 'ERROR',
                     'CRITICAL'.

    Return:
        Callable: A function to output log.
    """
    level = level.upper()
    if level == 'DEBUG':
        return logger.debug
    elif level == 'INFO':
        return logger.info
    elif level == 'WARNING':
        return logger.warning
    elif level == 'ERROR':
        return logger.error
    elif level == 'CRITICAL':
        return logger.critical
    else:
        return logger.info


def is_request_instance(request: Any) -> bool:
    """ Check is django request instance or not """
    django_request_objects: Tuple[Any, ...] = (HttpRequest, Request)
    return isinstance(request, django_request_objects)
