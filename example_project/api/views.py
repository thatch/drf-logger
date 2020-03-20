import datetime
from logging import getLogger

from django.http import HttpResponse, JsonResponse
from django.views import View
from drf_logger.decorators import APILoggingDecorator
from drf_logger.mixins import APILoggingMixin
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api import serializers
from api.models import Person

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


class PersonAPIView(APIView):

    @api_logger
    def post(self, request):
        serializer = serializers.PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            additional = {'message': 'kw'}
            res = Response(serializer.data, status=status.HTTP_201_CREATED)
            return res, additional

        additional = {'message': 'kw', 'level': 'ERROR'}
        res = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return res, additional


@api_logger
def django_json(request):
    data = {'name': 'django_json'}
    additional = {'message': 'I am from json response.'}
    return JsonResponse(data), additional


@api_logger
def http_now(request):
    now = datetime.datetime.now()
    msg = f'datetime: {now}'
    additional = {'message': 'kw', 'level': 'INFO'}
    return HttpResponse(msg, content_type='text/plain'), additional


class DjangoView(View):

    @api_logger
    def get(self, request, *args, **kwargs):
        additional = {'message': 'I am DjangoView'}
        return JsonResponse({'message': 'I am django boy.'}), additional


class MixinClassBasedView(APILoggingMixin, View):

    def get(self, request, *args, **kwargs):
        additional = {'message': 'I am MixinView'}
        return JsonResponse({'message': 'Hello mixin.'}), additional
