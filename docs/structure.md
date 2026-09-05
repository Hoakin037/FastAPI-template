# Структура проекта

## Корень

- `main.py` - точка запуска приложения через Uvicorn.
- `pyproject.toml` - зависимости Poetry, pytest-настройки и метаданные проекта.
- `ruff.toml` - правила линтинга и форматирования.
- `.env.example` - переменные окружения для полной Docker-сборки.
- `.env.test.example` - переменные окружения для локального запуска через
  `main.py` при инфраструктуре в Docker.
- `deploy/` - Dockerfile, compose-файлы и shell-entrypoint.
- `alembic/` - настройки и версии миграций.
- `tests/` - тесты базовых репозиториев и middleware.

## app/config

Настройки приложения разделены по файлам:

- `project.py` - host, port, CORS, имя проекта, версия, режим reload, уровень логов.
- `postgres.py` - подключение к PostgreSQL и сборка async DSN.
- `redis.py` - подключение к Redis.
- `s3.py` - подключение к S3/MinIO.
- `main.py` - агрегирующий `Settings`.
- `deps.py` - DI-фабрики конфигурации.

## app/server

- `core/app.py` - создание FastAPI-приложения, exception handlers,
  middleware, pagination.
- `core/router.py` - корневой API-роутер.
- `core/lifespan.py` - lifecycle-хуки приложения.
- `middleware/exception.py` - централизованная обработка исключений.

## app/infrastructure

Низкоуровневые клиенты и технические компоненты:

- `storage/postgres/` - engine, session provider, enum схем PostgreSQL,
  утилиты metadata/table args.
- `storage/s3/` - S3-клиент и DI.
- `cache/redis/` - Redis-клиент и DI.
- `logger/` - настройка логирования.
- `decorators/` - технические декораторы, включая логирование вызовов.

## app/shared

Общий слой, который не принадлежит конкретному доменному модулю:

- `interfaces/repositories/` - контракты базовых репозиториев.
- `repositories/` - реализации базовых PostgreSQL/Redis/S3-репозиториев.
- `schemas/` - базовые Pydantic-схемы, пагинация, сортировка, фильтры.
- `models/` - базовая SQLAlchemy-модель.
- `errors/` - модель ошибки, коды и исключение `BackendException`.
- `utils/` - общие функции ответа и пагинации.
- `consts/` - общие enum-значения.

## app/modules

Доменные модули. Сейчас шаблон содержит пример `users`:

- `models/` - SQLAlchemy-модели.
- `schemas/` - Pydantic DTO для API и внутренних слоев.
- `filters/` - фильтры для запросов.
- `interfaces/` - контракты слоя модуля.
- `repositories/` - доступ к данным.
- `services/` - бизнес-логика.
- `routes/` - FastAPI endpoints и OpenAPI responses.
- `consts/` - enum-значения модуля.

Новые домены стоит добавлять рядом с `users`, сохраняя такой же вертикальный
набор каталогов.
