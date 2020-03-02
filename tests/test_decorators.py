import logging
import os
from typing import Callable
import unittest

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from rest_framework.response import Response

import drf_logger.utils
from drf_logger.decorators import APILoggingDecorator, _get_logging_function

factory = APIRequestFactory()

logger = drf_logger.utils.get_default_logger(__name__)


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


class APILoggingDecoratorTests(unittest.TestCase):

    def setUp(self):
        self.logger = drf_logger.utils.get_default_logger(
            __name__,
            format_='simple'
        )
        self.api_logger = APILoggingDecorator(logger=self.logger)

    def test_simple(self):
        """ Check a dtype of return value and status_code """
        @self.api_logger
        def mock_api(request):
            additional = {'message': 'A message.', 'level': 'INFO'}
            return Response({'message': 'ok'}), additional

        http_request = factory.get('/')
        request = Request(http_request)
        ret = mock_api(request)

        self.assertIsInstance(ret, Response)
        self.assertEqual(ret.status_code, 200)

    def test_logger_not_logger(self):
        """ If api_logger get str as logger """
        api_logger = APILoggingDecorator(logger='I am logger.')

        @api_logger
        def mock_api(request):
            message_for_logger = 'A message from mock_api.'
            additional = {'message': message_for_logger, 'level': 'INFO'}
            return Response({'message': 'ok'}), additional

        http_request = factory.get('/')
        request = Request(http_request)
        ret = mock_api(request)

        self.assertIsInstance(ret, Response)
        self.assertEqual(ret.status_code, 200)

    def test_api_without_level(self):
        """ Return dict with only key: message """
        @self.api_logger
        def mock_api(request):
            message_for_logger = 'A message from mock_api.'
            additional = {'message': message_for_logger}
            return Response({'message': 'ok'}), additional

        http_request = factory.get('/')
        request = Request(http_request)
        ret = mock_api(request)

        self.assertIsInstance(ret, Response)
        self.assertEqual(ret.status_code, 200)

    def test_api_without_message(self):
        """ Return dict with only key: level """
        @self.api_logger
        def mock_api(request):
            additional = {'level': 'INFO'}
            return Response({'message': 'ok'}), additional

        http_request = factory.get('/')
        request = Request(http_request)
        ret = mock_api(request)

        self.assertIsInstance(ret, Response)
        self.assertEqual(ret.status_code, 200)

    def test_api_invalid_level(self):
        """ A test for invalid level. """
        @self.api_logger
        def mock_api(request):
            message = 'Invalid level.'
            additional = {'message': message, 'level': 'INVALID_LEVEL'}
            return Response({'message': 'ok'}), additional

        http_request = factory.get('/')
        request = Request(http_request)
        ret = mock_api(request)

        self.assertIsInstance(ret, Response)
        self.assertEqual(ret.status_code, 200)
