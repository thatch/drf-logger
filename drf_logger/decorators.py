import logging
import time
import warnings
from typing import Any, Callable, Dict, Tuple

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
            return_values = func(request, *args, **kwargs)
            processing_time: float = time.time() - time_start
            extra['processing_time']: str = f'{processing_time:.3e}'

            # The view returns only response object.
            if not isinstance(return_values, tuple):
                response = return_values

                msg = f'API: {extra["function"]} only returns ' \
                      f'{type(response)}. If you attatch ' \
                      'drf_logger.decorators.APILoggingDecorator to your ' \
                      'views, you should return additional logging context' \
                      ' like {"message": "Hello.", "level": "INFO"}.'
                warnings.warn(msg)

                extra['status_code']: int = response.status_code
                log_func = _get_logging_function(self.logger, 'INFO')
                log_func(msg='', extra=extra)
                return response

            response = return_values[0]
            ctx: Dict[str, Any] = return_values[1]

            extra['status_code']: int = response.status_code

            msg: str = ctx.get('message', '')
            level: str = ctx.get('level', LOG_LEVELS[1])

            log_func = _get_logging_function(self.logger, level)
            log_func(msg, extra=extra)
            return response

        return wrapper
