FROM python:3.13

WORKDIR /app/

RUN pip install poetry==2.0.0

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

RUN poetry install

COPY . .
ENV PYTHONPATH=.

