import unittest
from typing import Dict

from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from drf_logger import utils
from drf_logger._utils import (
    _get_client_ip, _get_logging_function, _is_request_instance
)
from rest_framework.request import Request

logger = utils.get_default_logger(__name__)


class GetLoggingFunctionTests(unittest.TestCase):

    def test_simple(self):
        """ A simple test """
        levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        for level in levels:
            ret_func = _get_logging_function(logger, level)
            expected = getattr(logger, level.lower())
            self.assertEqual(ret_func, expected)

    def test_invalid_level(self):
        """ If invalid level passed. """
        ret_func = _get_logging_function(logger, 'invalid_level')
        self.assertEqual(ret_func, logger.info)


class IsRequestInstanceTests(unittest.TestCase):

    def test_django_http_request(self):
        """ django.http.HttpRequest """
        request = HttpRequest()
        self.assertTrue(_is_request_instance(request))

    def test_drf_request(self):
        """ rest_framework.request.Request """
        request = Request(HttpRequest())
        self.assertTrue(_is_request_instance(request))

    def test_django_wsgi_request(self):
        """ rest_framework.request.Request """
        request = WSGIRequest({'REQUEST_METHOD': 'GET', 'wsgi.input': ''})
        self.assertTrue(_is_request_instance(request))


class GetClientIpTests(unittest.TestCase):

    def test_simple(self):
        params: Dict[str, str] = {
            'REQUEST_METHOD': 'GET',
            'wsgi.input': '',
            'REMOTE_ADDR': '127.0.0.0'
        }
        request = WSGIRequest(params)
        ip = _get_client_ip(request)
        assert ip == params['REMOTE_ADDR']
