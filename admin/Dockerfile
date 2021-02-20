FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ENV PYTHONUNBUFFERED 1

RUN pip install poetry

COPY ./src /app/src
COPY poetry.lock /app
COPY pyproject.toml /app

WORKDIR /app
RUN poetry config virtualenvs.create false
RUN poetry install