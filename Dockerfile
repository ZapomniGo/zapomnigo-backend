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

EXPOSE 8000

CMD ["gunicorn", "src.main:app", "-b", "0.0.0.0:8000", "--certfile", "data/certs/zapomnigo.crt", "--keyfile", "data/certs/zapomnigo.key", "-w", "4", "--access-logfile", "-", "--error-logfile", "src/shared/logfile.log"]