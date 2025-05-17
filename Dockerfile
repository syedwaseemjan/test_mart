FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/test_mart

WORKDIR /test_mart

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy Poetry files first for dependency caching
COPY pyproject.toml poetry.lock* README.md ./

RUN poetry config virtualenvs.create false
COPY . .
RUN poetry install --no-interaction --no-ansi $(test "$DEBUG" = "True" && echo "--with dev")

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
