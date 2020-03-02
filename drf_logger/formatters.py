import json
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
        """
        Notes:
            ex) A message., function=module.func, user_id=1, status_code=200
        """
        extra_txt = ''
        for k, v in record.__dict__.items():
            if k not in KEYS_TO_IGNORE:
                extra_txt += ', {}={}'.format(k, v)
        message = super().format(record)
        return message + extra_txt


class JSONExtraFormatter(Formatter):

    def format(self, record) -> str:
        """
        Notes:
            ex) {"This is a message": "A message.", "function": "module.func",
                 "user_id": 1, "status_code": 200}
        """
        dict_to_record = {}
        message = super().format(record)
        dict_to_record['message'] = message

        for k, v in record.__dict__.items():
            if k not in KEYS_TO_IGNORE:
                dict_to_record[k] = v

        return json.dumps(dict_to_record)
