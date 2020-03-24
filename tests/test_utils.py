import logging
import unittest

from drf_logger import utils


class GetDefaultLoggerTests(unittest.TestCase):

    def test_returned_dtype(self):
        """ Check a dtype of returned value. """
        logger = utils.get_default_logger(__name__)
        self.assertIsInstance(logger, logging.Logger)
