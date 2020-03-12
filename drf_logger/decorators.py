import logging
import warnings
from typing import Callable

from django.http import HttpRequest
from rest_framework.request import Request

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
        return logger.info


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
        def wrapper(request, *args, **kwargs):

            # In case decorator used in class based views like
            # rest_framework.viewsets.ModelViewSet, rest_framework.APIView.
            if not isinstance(request, (HttpRequest, Request)):
                if len(args) >= 1:
                    if isinstance(args[0], Request):
                        request = args[0]

            extra = {}
            extra['function'] = func.__module__ + '.' + func.__qualname__

            # request.user is django User model or
            # django.contrib.auth.models.AnonymousUser.
            if isinstance(request, (HttpRequest, Request)):
                extra['user_id'] = request.user.id

            return_values = func(request, *args, **kwargs)
            # The view returns only response object.
            if not isinstance(return_values, tuple):
                response = return_values

                msg = f'API: {extra["function"]} only returns ' \
                      f'{type(response)}. If you attatch ' \
                       'drf_logger.decorators.APILoggingDecorator to your ' \
                       'views, you should return additional logging context' \
                       ' like {"message": "Hello.", "level": "INFO"}.'
                warnings.warn(msg)

                extra['status_code'] = response.status_code
                log_func = _get_logging_function(self.logger, 'INFO')
                log_func(msg='', extra=extra)
                return response

            response = return_values[0]
            additionals = return_values[1]

            extra['status_code'] = response.status_code

            message = additionals.get('message', '')
            level = additionals.get('level', LOG_LEVELS[1])

            log_func = _get_logging_function(self.logger, level)
            log_func(message, extra=extra)
            return response

        return wrapper
