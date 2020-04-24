import os
import unittest

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

import drf_logger.utils
from drf_logger.decorators import APILoggingDecorator

factory = APIRequestFactory()

logger = drf_logger.utils.get_default_logger(__name__)


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
            return Response({'message': 'ok'})

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
            return Response({'message': 'ok'})

        http_request = factory.get('/')
        request = Request(http_request)
        ret = mock_api(request)

        self.assertIsInstance(ret, Response)
        self.assertEqual(ret.status_code, 200)

    def test_class_based_view(self):
        """ A test for class based view.
            Class based views pass it-self for arguments.
        """
        class MockAPIView(APIView):

            @self.api_logger
            def get(self, request):
                return Response({})

        request = factory.get('/')
        mock_view = MockAPIView.as_view()
        ret = mock_view(request)

        self.assertIsInstance(ret, Response)
        self.assertEqual(ret.status_code, 200)
