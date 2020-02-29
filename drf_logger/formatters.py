from logging import Formatter

# These keys are ignored in SimpleExtraFormatter.
KEYS_TO_IGNORE = (
    'args', 'created', 'exc_info', 'exc_text', 'family', 'fd', 'filename',
    'funcName', 'laddr', 'levelname', 'levelno', 'lineno', 'msecs', 'msg',
    'module', 'name', 'pathname', 'process', 'processName', 'proto', 'raddr',
    'relativeCreated', 'request', 'stack_info', 'thread', 'threadName', 'type'
)


class SimpleExtraFormatter(Formatter):

    def format(self, record) -> str:
        extra_txt = ''
        for k, v in record.__dict__.items():
            if k not in KEYS_TO_IGNORE:
                extra_txt += ', {}={}'.format(k, v)
        message = super().format(record)
        return message + extra_txt
