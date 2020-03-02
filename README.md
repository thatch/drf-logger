# drf-logger

![GitHub Actions](https://github.com/yutayamazaki/drf-logger/workflows/Python%20package/badge.svg)
[![PyPI Version](https://img.shields.io/pypi/v/drf-logger.svg)](https://pypi.org/project/drf-logger/)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
![GitHub Starts](https://img.shields.io/github/stars/yutayamazaki/drf-logger.svg?style=social)
![GitHub Forks](https://img.shields.io/github/forks/yutayamazaki/drf-logger.svg?style=social)

## Description

- This is a Python package that can easily get information such as status_code, user_id, the name of function etc. just by attaching a decorator.
- Recently, drf-logger supports `rest_framework.decorators.api_view` and` rest_framework.viewsets.ModelViewSet`.


## Installation

```shell
pip install drf-logger
```


## Example

- Write your API with Django Rest Framework and drf-logger.

```python
import drf_logger
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Load logging.Logger object.
logger = drf_logger.utils.get_default_logger(__name__)
# Create api_logger decorator.
api_logger = drf_logger.decorators.APILoggingDecorator(logger)


@api_view(['GET'])
@api_logger
def hello_api(request):
    message = 'This is a message from hello_api.'
    additional = {'message': message}
    return Response({'message': 'hello'}), additional
```

- Then, you can get log like follows.

```text
This is a message from hello_api., function=app.views.hello_api, user_id=1, status_code=200
```

- You can use APILoggingDecorator in ModeViewSet too.

```python
class PersonViewSet(viewsets.ModelViewSet):

    queryset = Person.objects.all()
    serializer_class = serializers.PersonSerializer

    @api_logger
    def list(self, request):
        queryset = Person.objects.all()
        serializer = serializers.PersonSerializer(queryset, many=True)
        additional = {'message': 'message from list', 'level': 'WARNING'}
        return Response(serializer.data), additional
```

```shell
message from list, function=app.views.PersonViewSet.list, user_id=1, status_code=200
```

## A procedure to register to PyPI.

```shell
# Install dependencies.
pip install twine
pip install check-manifest
# Check files before upload.
check-manifest
pip install wheel
# Build
python setup.py sdist bdist_wheel
# Upload to PyPI.
twine upload dist/*
```
