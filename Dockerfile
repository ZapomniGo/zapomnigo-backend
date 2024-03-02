FROM python:3.11 as build
RUN apt update
RUN pip install poetry

WORKDIR /app

COPY . .
RUN poetry install

FROM build as final

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["hypercorn", "src.main:asgi_app", "--bind","0.0.0.0:8000", "--workers", "4"]