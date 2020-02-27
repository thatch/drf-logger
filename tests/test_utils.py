import logging
import unittest

import drf_logger.utils


class GetDefaultLoggerTests(unittest.TestCase):

    def test_returned_dtype(self):
        """ Check a dtype of returned value. """
        logger = drf_logger.utils.get_default_logger(__name__)
        self.assertIsInstance(logger, logging.Logger)
