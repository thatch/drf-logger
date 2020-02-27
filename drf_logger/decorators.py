import logging
from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response

from drf_logger import utils

deco_logger = utils.get_default_logger(__name__)


def _get_logging_function(logger: logging.Logger, level: str) -> Callable:
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
        raise ValueError(f'Invalid logging level: {level}.')


class APILoggingDecorator(object):

    def __init__(self, logger=None, level: str = 'INFO'):
        if not isinstance(logger, logging.Logger):
            logger = deco_logger
        self.log_func = _get_logging_function(logger, level)

    def __call__(self, func: Callable) -> Callable:
        def wrapper(request: Request, **kwargs) -> Response:
            extra = {}
            extra['user_id'] = request.user.id

            response, message = func(request, **kwargs)

            extra['status_code'] = response.status_code
            extra['function'] = func.__name__

            self.log_func(message, extra=extra)
            return response

        return wrapper
