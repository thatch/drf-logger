import logging
import os
from typing import Callable
import unittest

import django
from rest_framework.request import Request
from rest_framework.response import Response
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()
from rest_framework.test import APIRequestFactory

import drf_logger.utils
from drf_logger.decorators import APILoggingDecorator, _get_logging_function

factory = APIRequestFactory()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = drf_logger.utils.SimpleExtraFormatter()
ch.setFormatter(formatter)
logger.addHandler(ch)


class GetLoggingFunctionTests(unittest.TestCase):

    def test_simple(self):
        """ A simple test """
        levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        for level in levels:
            ret_func = _get_logging_function(logger, level)
            expected = eval(f'logger.{level.lower()}')
            self.assertEqual(ret_func, expected)

    def test_raise(self):
        """ If invalid level passed. """
        with self.assertRaises(ValueError) as e:
            _get_logging_function(logger, 'invalid level')


class APILoggingDecoratorTests(unittest.TestCase):

    def setUp(self):
        self.api_logger = APILoggingDecorator(logger=logger)

    def test_simple(self):
        """ Check a dtype of return value and status_code """
        @self.api_logger
        def mock_api(request):
            message_for_logger = 'A message.'
            return Response({'message': 'ok'}), message_for_logger

        http_request = factory.get('/')
        request = Request(http_request)
        ret = mock_api(request)

        self.assertIsInstance(ret, Response)
        self.assertEqual(ret.status_code, 200)

    def test_logger_not_logger(self):
        """ If api_logger get str as logger """
        api_logger = APILoggingDecorator(logger='I am logger.')

        @api_logger
        def mock_api_error(request):
            message_for_logger = 'A message from sample_api.'
            return Response({'message': 'ok'}), message_for_logger

        http_request = factory.get('/')
        request = Request(http_request)
        ret = mock_api_error(request)

        self.assertIsInstance(ret, Response)
        self.assertEqual(ret.status_code, 200)
