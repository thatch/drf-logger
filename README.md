# drf-logger

![GitHub Actions](https://github.com/yutayamazaki/drf-logger/workflows/Python%20package/badge.svg)

## Example

- Write your API with Django Rest Framework and drf-logger.

```python
import logging

import drf_logger
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = drf_logger.utils.SimpleExtraFormatter()
ch.setFormatter(formatter)
logger.addHandler(ch)

api_logger = drf_logger.APILoggingDecorator(logger)


@api_logger
@api_view(['GET'])
def sample_api(request):
    message_for_logger = 'A message from sample_api.'
    return Response({'message': 'hello'}), message_for_logger
```

- Then, you can get log like follows.

```text
A message from sample_api., user_id=None, status_code=200, function=sample_api
```
