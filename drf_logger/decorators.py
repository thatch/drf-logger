import logging
from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response

from drf_logger import utils

deco_logger = utils.get_default_logger(__name__)

LOG_LEVELS = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')


def _get_logging_function(logger: logging.Logger, level: str) -> Callable:
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
        raise ValueError(f'Invalid logging level: {level}.')


class APILoggingDecorator(object):

    """ APILoggingDecorator is a decorator for APIs of DRF.

    Args:
        logger (logging.Logger): A logger instance.
        level (str): A logging level used as default.
    """

    def __init__(self, logger=None, level: str = 'INFO'):
        if not isinstance(logger, logging.Logger):
            logger = deco_logger
        self.logger = logger

    def __call__(self, func: Callable) -> Callable:
        def wrapper(request: Request, *args, **kwargs) -> Response:
            extra = {}
            extra['function'] = func.__module__ + '.' + func.__qualname__

            # If this decorator used in APIViewSet, request comes as
            # APIViewSet. And APIViewSet has not attribute user.
            # request.user is django User model or
            # django.contrib.auth.models.AnonymousUser.
            if isinstance(request, Request):
                extra['user_id'] = request.user.id

            response, additionals = func(request, *args, **kwargs)

            message = additionals.get('message', '')
            level = additionals.get('level', LOG_LEVELS[1])

            if level.upper() not in LOG_LEVELS:
                level = 'INFO'
            log_func = _get_logging_function(self.logger, level)

            extra['status_code'] = response.status_code

            log_func(message, extra=extra)
            return response

        return wrapper
