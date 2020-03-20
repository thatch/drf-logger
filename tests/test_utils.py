import logging
import unittest

from drf_logger import utils

logger = utils.get_default_logger(__name__)


class GetDefaultLoggerTests(unittest.TestCase):

    def test_returned_dtype(self):
        """ Check a dtype of returned value. """
        logger = utils.get_default_logger(__name__)
        self.assertIsInstance(logger, logging.Logger)


class GetLoggingFunctionTests(unittest.TestCase):

    def test_simple(self):
        """ A simple test """
        levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        for level in levels:
            ret_func = utils.get_logging_function(logger, level)
            expected = getattr(logger, level.lower())
            self.assertEqual(ret_func, expected)

    def test_invalid_level(self):
        """ If invalid level passed. """
        ret_func = utils.get_logging_function(logger, 'invalid_level')
        self.assertEqual(ret_func, logger.info)
