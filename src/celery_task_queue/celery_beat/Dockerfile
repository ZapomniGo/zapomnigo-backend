FROM python:3.11 as build
LABEL authors="ivanobreshkov"

RUN apt update
RUN pip install poetry

WORKDIR /app

COPY . .
RUN poetry install

FROM build as final

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

CMD ["celery", "-A", "src.celery_task_queue.make_celery", "beat", "--loglevel", "INFO"]