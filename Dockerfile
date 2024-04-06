FROM python:3.11-buster as builder
LABEL authors="ivanobreshkov"

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster as runtime

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY shared ./shared
COPY src ./src
COPY data ./data
COPY resources ./resources
COPY .env ./
COPY health_check.sh ./

RUN chmod +x health_check.sh

EXPOSE 8000

CMD ["gunicorn", "src.main:app", "-b", "0.0.0.0:8000", "--certfile", "data/certs/zapomnigo.crt", "--keyfile", "data/certs/zapomnigo.key", "-w", "4", "--access-logfile", "-", "--error-logfile", "src/shared/logfile.log"]