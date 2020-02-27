import logging

BUILDIN_KEYS = (
    'args', 'created', 'exc_info', 'exc_text', 'filename', 'funcName',
    'levelname', 'levelno', 'lineno', 'msecs', 'msg', 'module', 'name',
    'pathname', 'process', 'processName', 'relativeCreated', 'stack_info',
    'thread', 'threadName',
)


class SimpleExtraFormatter(logging.Formatter):

    def format(self, record) -> str:
        extra_txt = ''
        for k, v in record.__dict__.items():
            if k not in BUILDIN_KEYS:
                extra_txt += ', {}={}'.format(k, v)
        message = super().format(record)
        return message + extra_txt


def get_default_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = SimpleExtraFormatter()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
