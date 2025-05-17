SHELL := /bin/bash

# Variables definitions
# -----------------------------------------------------------------------------

ifeq ($(TIMEOUT),)
TIMEOUT := 60
endif

# Local: docker
# -----------------------------------------------------------------------------
.PHONY: test lint migrate migration docker install run generate_dot_env

test:
	docker-compose exec app poetry run pytest tests -vv --show-capture=all

lint:
	@echo "Running all linters inside Docker..."
	docker-compose exec app sh -c "\
		poetry run black . && \
		poetry run isort . && \
		poetry run ruff check . && \
		poetry run mypy . \
	"
	@echo "Linting complete!"

migrate:
	docker-compose exec app poetry run alembic upgrade head

migration:
	@read -p "Enter migration message: " msg; \
	docker-compose exec app poetry run alembic revision --autogenerate -m "$$msg"

demo_data:
	docker-compose exec app poetry run python scripts/demo_data.py

flush_db:
	@echo "Flushing MySQL database..."
	@docker-compose exec db mysql -u$$(docker-compose exec db printenv MYSQL_USER) \
		-p$$(docker-compose exec db printenv MYSQL_PASSWORD) \
		-e "DROP DATABASE IF EXISTS $$(docker-compose exec db printenv MYSQL_DATABASE); \
		    CREATE DATABASE $$(docker-compose exec db printenv MYSQL_DATABASE);"
	@echo "Database flushed and recreated!"

reset_db: flush_db migrate demo_data
	@echo "Database reset complete with migrations and demo data!"

# Local: direct on the OS
# -----------------------------------------------------------------------------
install: generate_dot_env
	# poetry install --with dev,aws
	poetry install --with dev

run:
	PYTHONPATH=app/ poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8080

generate_dot_env:
	poetry run python scripts/generate_env.py