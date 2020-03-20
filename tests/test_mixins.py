import os
import unittest

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

import drf_logger
from drf_logger import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()


class APILoggingMixinTests(unittest.TestCase):

    def setUp(self):
        self.logger = drf_logger.utils.get_default_logger(
            __name__,
            format_='simple'
        )

    def test_simple(self):
        """ Simple test on class based view. """
        class MockAPIView(mixins.APILoggingMixin, APIView):

            def get(self, request):
                return Response({})

        request = factory.get('/')
        mock_view = MockAPIView.as_view()
        ret = mock_view(request)

        assert isinstance(ret, Response)
        assert ret.status_code == 200
