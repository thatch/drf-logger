import logging
import warnings
from typing import Any, Callable, Tuple

from django.http import HttpRequest
from django.utils import timezone
from rest_framework.request import Request

from drf_logger import utils

deco_logger = utils.get_default_logger(__name__)

LOG_LEVELS = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')


def is_request_instance(request: Any) -> bool:
    """ Check is django request instance or not """
    django_request_objects: Tuple[Any, ...] = (HttpRequest, Request)
    return isinstance(request, django_request_objects)


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
            request_obj = request
            if not is_request_instance(request_obj):
                if len(args) >= 1:
                    if is_request_instance(args[0]):
                        request_obj = args[0]

            extra = {}
            extra['function'] = func.__module__ + '.' + func.__qualname__
            extra['time'] = str(timezone.now())

            # request.user is django User model or
            # django.contrib.auth.models.AnonymousUser.
            if is_request_instance(request_obj):
                extra['user_id'] = request_obj.user.id
                extra['method'] = request_obj.method

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
                log_func = utils.get_logging_function(self.logger, 'INFO')
                log_func(msg='', extra=extra)
                return response

            response = return_values[0]
            additionals = return_values[1]

            extra['status_code'] = response.status_code

            message = additionals.get('message', '')
            level = additionals.get('level', LOG_LEVELS[1])

            log_func = utils.get_logging_function(self.logger, level)
            log_func(message, extra=extra)
            return response

        return wrapper
