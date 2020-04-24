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
    return Response({'message': 'hello'})


class PersonViewSet(viewsets.ModelViewSet):

    queryset = Person.objects.all()
    serializer_class = serializers.PersonSerializer

    @api_logger
    def list(self, request):
        queryset = Person.objects.all()
        serializer = serializers.PersonSerializer(queryset, many=True)
        return Response(serializer.data)


class PersonAPIView(APIView):

    @api_logger
    def post(self, request):
        serializer = serializers.PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = Response(serializer.data, status=status.HTTP_201_CREATED)
            return res

        res = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return res


@api_logger
def django_json(request):
    data = {'name': 'django_json'}
    return JsonResponse(data)


@api_logger
def http_now(request):
    now = datetime.datetime.now()
    msg = f'datetime: {now}'
    return HttpResponse(msg, content_type='text/plain')


class DjangoView(View):

    @api_logger
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'I am django boy.'})


class MixinClassBasedView(APILoggingMixin, View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Hello mixin.'})
