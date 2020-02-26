import logging
import os
import unittest

import django
from drf_logger.decorators import api_logger
from rest_framework.request import Request
from rest_framework.response import Response

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class ApiLoggerTests(unittest.TestCase):

    def test_simple(self):
        """ Check a dtype of return value and status_code """
        @api_logger(logger)
        def mock_api(request):
            message_for_logger = 'A message from sample_api.'
            return Response({'message': 'ok'}), message_for_logger

        http_request = factory.get('/')
        request = Request(http_request)
        ret = mock_api(request)

        self.assertIsInstance(ret, Response)
        self.assertEqual(ret.status_code, 200)

    def test_logger_not_logger(self):
        """ If api_logger get str as logger """
        @api_logger('I am logger.')
        def mock_api_error(request):
            message_for_logger = 'A message from sample_api.'
            return Response({'message': 'ok'}), message_for_logger

        http_request = factory.get('/')
        request = Request(http_request)
        ret = mock_api_error(request)

        self.assertIsInstance(ret, Response)
        self.assertEqual(ret.status_code, 200)
