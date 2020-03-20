# drf-logger

![GitHub Actions](https://github.com/yutayamazaki/drf-logger/workflows/Python%20package/badge.svg)
[![PyPI Version](https://img.shields.io/pypi/v/drf-logger.svg)](https://pypi.org/project/drf-logger/)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
![GitHub Starts](https://img.shields.io/github/stars/yutayamazaki/drf-logger.svg?style=social)
![GitHub Forks](https://img.shields.io/github/forks/yutayamazaki/drf-logger.svg?style=social)

## Features

- Logging satus_code, user_id, the name of function, message from view, etc just by attaching a decorator.
- Readable formatters for logging.Logger like `SimpleExtraFormatter`, `JSONExtraFormatter`.


## Description

- This is a Python package that can easily get information such as status_code, user_id, the name of function etc. just by attaching a decorator.


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

## What data can drf-logger fetch.

|  data  |  key  |  APILoggingDecorator  |  APILoggingMixin  |
|---|---|---|---|
|  name of the api  |  func  |  yes  |  no  |
|  ip address  |  ip  |  yes  |  yes  |
|  django user id  |  user_id  |  yes  |  yes  |
|  http method  |  method  |  yes  |  yes  |
|  status_code  |  status_code  |  yes  |  yes  |


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
