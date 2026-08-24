FROM python:3.13

WORKDIR /app/

RUN pip install poetry==2.0.0

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

RUN poetry install


COPY . .

ENV PYTHONPATH=.

COPY /deploy/init.sh /app/deploy/init.sh
RUN chmod +x /app/deploy/init.sh

CMD ["bash", "deploy/init.sh"]

