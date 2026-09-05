# Разработка

## Переменные окружения

Проект читает настройки из `.env` через `pydantic-settings`. Для полной
Docker-сборки используйте `.env.example`; для локального запуска приложения
через `main.py` при сервисах в Docker - `.env.test.example`.

Важные различия:

- Docker-режим использует имена контейнеров как host:
  `fastapi-template-postgres`, `fastapi-template-redis`,
  `http://fastapi-template-minio:9000`.
- Локальный режим использует `localhost` и проброшенные порты:
  PostgreSQL `5470`, Redis `6390`, MinIO API `9021`.

## Полная Docker-сборка

```bash
cp .env.example .env
docker compose -f ./deploy/.docker-compose.yaml up --build
```

Сервис `fastapi-template-app` запускает `deploy/init.sh`, который сначала
применяет миграции, затем стартует `python3 main.py`.

## Локальный запуск приложения

```bash
cp .env.test.example .env
docker compose -f ./deploy/.docker-compose.local.yaml up -d
poetry install
poetry run alembic upgrade head
poetry run python main.py
```

По умолчанию приложение слушает `http://localhost:8006`.

## Миграции

Создать новую миграцию:

```bash
poetry run alembic revision --autogenerate -m "migration name"
```

Применить миграции:

```bash
poetry run alembic upgrade head
```

Откатить последнюю миграцию:

```bash
poetry run alembic downgrade -1
```

## Тесты

```bash
poetry run pytest
```

Часть тестов зависит от доступности PostgreSQL, Redis или S3-совместимого
хранилища. Для интеграционных проверок перед запуском тестов поднимите
инфраструктуру через `deploy/.docker-compose.local.yaml`.

## Линтинг и форматирование

```bash
poetry run ruff check .
poetry run ruff check . --fix
poetry run ruff format .
```

Pre-commit конфигурация использует `ruff-check --fix` и `ruff-format`.
