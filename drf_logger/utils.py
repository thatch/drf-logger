import logging

BUILDIN_KEYS = (
    'args', 'created', 'exc_info', 'exc_text', 'filename', 'funcName',
    'levelname', 'levelno', 'lineno', 'msecs', 'msg', 'module', 'name',
    'pathname', 'process', 'processName', 'relativeCreated', 'stack_info',
    'thread', 'threadName',
)


class SimpleExtraFormatter(logging.Formatter):

    def format(self, record):
        extra_txt = ''
        for k, v in record.__dict__.items():
            if k not in BUILDIN_KEYS:
                extra_txt += ', {}={}'.format(k, v)
        message = super().format(record)
        return message + extra_txt
