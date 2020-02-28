from logging import getLogger

from drf_logger.decorators import APILoggingDecorator
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app import serializers
from app.models import Person

logger = getLogger('django')
api_logger = APILoggingDecorator(logger=logger, level='INFO')


@api_view(['GET'])
@api_logger
def hello_api(request):
    logger.info('I am in hello_api.')
    return Response({'message': 'hello'}), 'This is a message from drf-logger.'


class PersonViewSet(viewsets.ModelViewSet):

    queryset = Person.objects.all()
    serializer_class = serializers.PersonSerializer

    @api_logger
    def list(self, request):
        queryset = Person.objects.all()
        serializer = serializers.PersonSerializer(queryset, many=True)
        return Response(serializer.data), 'message from list'
