from logging import getLogger

from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_logger.decorators import APILoggingDecorator

logger = getLogger('django')
api_logger = APILoggingDecorator(logger=logger, level='INFO')


@api_view(['GET'])
@api_logger
def hello_api(request):
    logger.info('I am in hello_api.')
    return Response({'message': 'hello'}), 'This is a message from drf-logger.'
