import logging

from drf_logger.formatters import SimpleExtraFormatter


def get_default_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = SimpleExtraFormatter()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
