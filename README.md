# drf-logger

![GitHub Actions](https://github.com/yutayamazaki/drf-logger/workflows/Python%20package/badge.svg)
[![PyPI Version](https://img.shields.io/pypi/v/drf-logger.svg)](https://pypi.org/project/drf-logger/)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
![GitHub Starts](https://img.shields.io/github/stars/yutayamazaki/drf-logger.svg?style=social)
![GitHub Forks](https://img.shields.io/github/forks/yutayamazaki/drf-logger.svg?style=social)

## Features

- You can fetch information easily by like status_code, user_id, the name of function, request time, ip address, http method.
- APILogginDecorator is suitable for function-based views, APILoggingMixin is for class-based views.
- Readable formatters for logging.Logger like `SimpleExtraFormatter`, `JSONExtraFormatter`.


## Installation

```shell
pip install drf-logger
```


## What data can you get with drf-logger.

|  data  |  key  |  APILoggingDecorator  |  APILoggingMixin  |
| :---: | :---: | :---: | :---: |
|  name of the api  |  func  |  :white_check_mark:  |    |
|  ip address  |  ip  |  :white_check_mark:  |  :white_check_mark:  |
|  django user id  |  user_id  |  :white_check_mark:  |  :white_check_mark:  |
|  http method  |  method  |  :white_check_mark:  |  :white_check_mark:  |
|  status_code  |  status_code  |  :white_check_mark:  |  :white_check_mark:  |


## Example

- Example django project using drf-logger is available [here](https://github.com/yutayamazaki/drf-logger/tree/docs-mixin/example_project).

### How to use APILoggingDecorator

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
This is a message from hello_api., function=api.views.hello_api, time=2020-03-18 13:09:19.524105+00:00, ip=127.0.0.1, user_id=1, method=GET, status_code=200
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

### How to use APILoggingMixin

- If you use class-based views in django, you can use `APILoggingMixin`.

```python
from django.views import View
from drf_logger.mixins import APILoggingMixin


class MixinClassBasedView(APILoggingMixin, View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Hello mixin.'})

```

- You can get log like this.

```shell
, time=2020-03-24 16:55:45.794735+00:00, ip=127.0.0.1, user_id=null, method=GET, status_code=200
```


## Contributing
- You can see how to contribute to this project in [CONTRIBUTING.md](https://github.com/yutayamazaki/drf-logger/blob/master/CONTRIBUTING.md).


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

## Development
```bash
# in project root
% docker-compose up # you can develop drf-logger while running sample django app. http://localhost:8000
```
