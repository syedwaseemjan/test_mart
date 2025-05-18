# TestMart

A FastAPI-powered backend for an e-commerce admin dashboard providing sales analytics, revenue insights, and inventory management tools.

## Development Requirements

- Python 3.11+
- Poetry
- Docker

## Installation

```sh
make generate_dot_env (For quick setup, you can skip this step and use `cp .env.example .env`)
docker-compose build --no-cache
docker-compose up
make migrate
make demo_data
make lint
make test
```

## Running linting

`make lint`

## Running Tests

`make test`

## To flush all tables and re-add demo data

`make reset_db`

## Access Swagger Documentation

> <http://localhost:8080/docs>

## Access Redocs Documentation

> <http://localhost:8080/redoc>

## API Endpoints

### Products

* `POST /products/` — Register new product
* `GET /products/` — List products
* `GET /products/{product_id}` — Get product details

### Inventory

* `POST /inventory/` — Add inventory record
* `GET /inventory/` — List inventory status
* `GET /inventory/low-stock` — List products with low stock
* `PUT /inventory/{product_id}` — Update stock for product
* `GET /inventory/{product_id}/logs` — List inventory changes for product

### Sales

* `POST /sales/` — Record a sale
* `GET /sales?start_date=2025-01-14&end_date=2025-12-14&product_id=1&category=Electronics` — List sales with optional product_id, date and category filters
* `GET /sales/revenue?period=day|week|month|year` — Revenue aggregation
* `GET /sales//revenue/comparison?period=day|week|month|year&compare_periods=2&category=Electronics` — Revenue aggregation

## Project structure

Files related to application are in the `app` or `tests` directories.
Application parts are:

```
test_mart
├── pyproject.toml/          # Poetry dependency management and project configuration
├── Dockerfile/              # Container configuration for the FastAPI application
├── docker-compose/          # Multi-container setup (app + database)
├── alembic/                 # Database migration scripts and configuration
│   ├── versions/            # Individual migration files
│   └── env.py               # Migration environment setup

├── tests/                   # All test cases (unit/integration)
├── scripts/                 # Utility scripts (e.g., demo data generation)
│   └── generate_env.py      # Environment variable setup

├── app/                     # Core application code
│   ├── main.py              # FastAPI app initialization and middleware
│   ├── models.py            # SQLAlchemy database models
│   ├── database.py          # Database connection and session handling
│   ├── schemas.py           # Pydantic models for request/response validation
│   │
│   ├── routers/             # API endpoint controllers
│   │   ├── product.py       # Product-related routes (CRUD operations)
│   │   ├── sales.py         # Sales transactions endpoints
│   │   └── inventory.py     # Inventory management endpoints
```

## Database Schema

For detailed database documentation including table structures, relationships, and schema design:  
[Database Documentation](Database.md)  

## Notes

* Use MySQL with `pymysql` driver
* Alembic used for DB migrations
* Demo data covers 5 products with random inventory & sales