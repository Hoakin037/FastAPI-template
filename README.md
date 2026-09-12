# FastAPI Template

Шаблон асинхронного backend-сервиса на FastAPI. В проекте уже есть базовая
структура модулей, настройки через `.env`, PostgreSQL, Redis, S3-совместимое
хранилище MinIO, Alembic-миграции, общий слой ошибок, пагинация, фильтрация,
сортировка и пример доменного модуля `users`.

## Технологии

- Python 3.13
- FastAPI и Uvicorn
- SQLAlchemy 2.0 async, asyncpg, Alembic
- Pydantic v2 и pydantic-settings
- Redis async client
- aioboto3 для S3/MinIO
- Docker Compose
- Ruff, pytest

## Быстрый старт в Docker

1. Создайте `.env` из примера:

```bash
cp .env.example .env
```

2. Проверьте значения в `.env`. Для полной Docker-сборки оставьте хосты
   сервисов как в `.env.example`: `fastapi-template-postgres`,
   `fastapi-template-redis`, `http://fastapi-template-minio:9000`.

3. Соберите и запустите приложение со всеми зависимостями:

```bash
docker compose -f deploy/.docker-compose.local.yaml --env-file .env up  --build -d
```

Контейнер приложения сам применит миграции через `alembic upgrade head` и
запустит `python3 main.py`. API будет доступно на порту из `PORT`
по умолчанию `http://localhost:8006`.

## Тестовый локальный запуск через main.py

Этот режим запускает приложение на машине разработчика, а PostgreSQL, Redis и
MinIO поднимает в Docker.

1. Создайте локальный `.env`:

```bash
cp .env.test.example .env
```

2. Поднимите инфраструктуру без контейнера приложения:

```bash
docker compose -f ./deploy/.docker-compose.local.yaml up -d
```

3. Установите зависимости:

```bash
poetry install
```

4. Примените миграции:

```bash
poetry run alembic upgrade head
```

5. Запустите API:

```bash
poetry run python main.py
```

Swagger UI доступен по адресу `http://localhost:8006/docs`, OpenAPI-схема -
`http://localhost:8006/openapi.json`.

## Проверки

```bash
poetry run pytest
poetry run ruff check .
poetry run ruff format .
```

Если используете pre-commit:

```bash
poetry run pre-commit run --all-files
```

## Документация

- [docs/architecture.md](docs/architecture.md) - архитектура и поток запроса.
- [docs/structure.md](docs/structure.md) - структура каталогов и назначение слоев.
- [docs/development.md](docs/development.md) - локальная разработка, миграции, тесты.
