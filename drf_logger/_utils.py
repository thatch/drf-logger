import logging
from typing import Any, Callable, Tuple

from django.http import HttpRequest
from rest_framework.request import Request


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


def _is_request_instance(request: Any) -> bool:
    """ Check is django request instance or not """
    django_request_objects: Tuple[Any, ...] = (HttpRequest, Request)
    return isinstance(request, django_request_objects)


def _get_client_ip(request) -> str:
    """ Get client ip address from request instance. We can fetch ip address
        from these classes.
        - django.core.handlers.wsgi.WSGIRequest
        - rest_framework.request.Request
    """
    ip: str
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
