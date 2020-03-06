# Contributing Guidelines

## Coding Style

We can check coding style using flake8.

```shell
pip install -r requirements-dev.txt
flake8 drf_logger
mypy drf_logger

# When you use docker.
docker-compose run --rm django flake8 drf_logger example_project
docker-compose run --rm django mypy drf_logger
```

The above job contains following packages.

- [flake8](http://flake8.pycqa.org)
- [mypy](http://mypy-lang.org/)


## Testing

```shell
# Run tests and measure coverages.
coverage run -m unittest discover tests
# With docker-compose.
docker-compose run --rm django coverage run -m unittest discover tests

# Output coverage report.
coverage report -m
# With docker-compose.
docker-compose run --rm django coverage report -m
```
