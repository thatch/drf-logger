from django.utils import timezone
from drf_logger import utils

LOG_LEVELS = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')


class APILoggingMixin:

    logger = None

    def dispatch(self, request, *args, **kwargs):
        extra: dict = {}
        extra['time']: str = str(timezone.now())
        extra['ip']: str = utils.get_client_ip(request)
        extra['user_id'] = request.user.id
        extra['method']: str = request.method

        response = super().dispatch(request, *args, **kwargs)

        extra['status_code']: int = response.status_code
        if self.logger is None:
            self.logger = utils.get_default_logger(__name__)
        self.logger.info(msg='', extra=extra)

        return response
