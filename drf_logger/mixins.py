from django.utils import timezone
from drf_logger import utils

LOG_LEVELS = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')


class APILoggingMixin:

    logger = utils.get_default_logger(__name__)

    def dispatch(self, request, *args, **kwargs):
        extra = {}

        extra['time'] = str(timezone.now())
        extra['ip'] = utils.get_client_ip(request)
        extra['user_id'] = request.user.id
        extra['method'] = request.method

        response, ctx = super().dispatch(request, *args, **kwargs)

        extra['status_code']: int = response.status_code

        message = ctx.get('message', '')
        level = ctx.get('level', LOG_LEVELS[1])

        log_func = utils.get_logging_function(self.logger, level)
        log_func(message, extra=extra)

        return response
