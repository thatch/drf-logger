import logging
import time
from typing import Callable, Tuple

from django.utils import timezone

from drf_logger import utils
from drf_logger._utils import (
    _get_client_ip, _get_logging_function, _is_request_instance
)

LOG_LEVELS: Tuple[str, ...] = (
    'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
)

deco_logger = utils.get_default_logger(__name__)


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
        self.level = level

    def __call__(self, func: Callable) -> Callable:
        def wrapper(request, *args, **kwargs):

            # In case decorator used in class based views like
            # rest_framework.viewsets.ModelViewSet, rest_framework.APIView.
            request_obj = request
            if not _is_request_instance(request_obj):
                if len(args) >= 1:
                    if _is_request_instance(args[0]):
                        request_obj = args[0]

            extra = {}
            extra['function']: str = func.__module__ + '.' + func.__qualname__
            extra['time']: str = str(timezone.now())
            extra['ip']: str = _get_client_ip(request_obj)

            # request.user is django User model or
            # django.contrib.auth.models.AnonymousUser.
            if _is_request_instance(request_obj):
                extra['user_id'] = request_obj.user.id
                extra['method']: str = request_obj.method

            time_start: float = time.time()

            response = func(request, *args, **kwargs)

            processing_time: float = time.time() - time_start
            extra['processing_time']: str = f'{processing_time:.3e}'
            extra['status_code']: int = response.status_code

            log_func = _get_logging_function(self.logger, self.level)
            log_func('', extra=extra)
            return response

        return wrapper
