# TestMart

A FastAPI-powered backend for an e-commerce admin dashboard providing sales analytics, revenue insights, and inventory management tools.

## Development Requirements

- Python 3.11+
- Docker

## Installation

```sh
docker-compose build --no-cache
docker-compose up
make migrate
make lint
make test
```

## Running linting

`make lint`

## Running Tests

`make test`

## Access Swagger Documentation

> <http://localhost:8080/docs>

## Access Redocs Documentation

> <http://localhost:8080/redoc>

## Project structure

Files related to application are in the `app` or `tests` directories.
Application parts are:

```
test_mart
├──poetry.toml/
├──pyproject.toml/
├──Dockerfile/
├──docker-compose/
├──Dockerfile/
├──alembic/
├──tests/
├──scripts/
├──app/
│  ├── main.py
│  ├── models.py
│  ├── database.py
│  ├── schemas.py
│  ├── routers/
│  │   ├── __init__.py
│  │   ├── product.py
│  │   ├── sales.py
│  │   └── inventory.py
```

