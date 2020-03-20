import logging
import unittest

from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from drf_logger import utils
from rest_framework.request import Request

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


class IsRequestInstanceTests(unittest.TestCase):

    def test_django_http_request(self):
        """ django.http.HttpRequest """
        request = HttpRequest()
        self.assertTrue(utils.is_request_instance(request))

    def test_drf_request(self):
        """ rest_framework.request.Request """
        request = Request(HttpRequest())
        self.assertTrue(utils.is_request_instance(request))

    def test_django_wsgi_request(self):
        """ rest_framework.request.Request """
        request = WSGIRequest({'REQUEST_METHOD': 'GET', 'wsgi.input': ''})
        self.assertTrue(utils.is_request_instance(request))
