# Stage 1: Building the dependencies
FROM python:3.10-slim AS builder

WORKDIR /app

# Copy the poetry.lock and pyproject.toml files
COPY ../poetry.lock ../pyproject.toml ./

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Stage 2: Running the shell script
FROM python:3.10-slim

WORKDIR /app
COPY . ./

# Copy the installed dependencies from the previous stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# ENTRYPOINT uvicorn --host 0.0.0.0 api:app
CMD uvicorn http_server:app --reload --host 0.0.0.0 --port 8000
