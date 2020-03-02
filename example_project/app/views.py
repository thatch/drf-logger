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
    message = 'This is a message from hello_api.'
    additional = {'message': message}
    return Response({'message': 'hello'}), additional


class PersonViewSet(viewsets.ModelViewSet):

    queryset = Person.objects.all()
    serializer_class = serializers.PersonSerializer

    @api_logger
    def list(self, request):
        queryset = Person.objects.all()
        serializer = serializers.PersonSerializer(queryset, many=True)
        additional = {'message': 'message from list', 'level': 'WARNING'}
        return Response(serializer.data), additional
