import logging

deco_logger = logging.getLogger(__name__)
deco_logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
deco_logger.addHandler(ch)


def api_logger(logger=None):
    if not isinstance(logger, logging.Logger):
        logger = deco_logger

    def wrapper(func):
        def _wrapper(request, **kwargs):
            extra = {}
            extra['user_id'] = request.user.id

            response, message = func(request, **kwargs)

            extra['status_code'] = response.status_code
            extra['function'] = func.__class__.__name__

            logger.info(message, extra=extra)
            return response
        return _wrapper
    return wrapper
