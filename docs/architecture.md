# Архитектура

## Обзор

`FastAPI Template` - модульный асинхронный backend-шаблон. Приложение
запускается из `main.py`, где Uvicorn поднимает объект
`app.server.core.app:app`.

```
HTTP client
    |
    v
main.py -> uvicorn -> app.server.core.app:app
    |
    +-- middleware: CORS, ExceptionMiddleware
    |
    +-- app.server.core.router:api, prefix /api
            |
            +-- app.modules.users.routes.user:router
                    |
                    +-- UserService
                            |
                            +-- IUserRepo -> UserRepo -> PostgreSQL
```

## Слои

| Слой | Назначение | Где находится |
|---|---|---|
| Server | Создание FastAPI-приложения, middleware, подключение роутеров | `app/server/` |
| Config | Настройки проекта и зависимости уровня конфигурации | `app/config/` |
| Infrastructure | Клиенты и низкоуровневая инфраструктура: PostgreSQL, Redis, S3, логирование | `app/infrastructure/` |
| Modules | Доменные модули приложения | `app/modules/` |
| Shared | Общие модели, схемы, ошибки, интерфейсы, базовые репозитории и утилиты | `app/shared/` |
| Alembic | Миграции базы данных | `alembic/` |
| Tests | Автотесты | `tests/` |

## Поток HTTP-запроса

1. `main.py` запускает Uvicorn с настройками из `ProjectSettings`.
2. `app/server/core/app.py` создает `FastAPI`, регистрирует exception handlers,
   CORS, общий `ExceptionMiddleware`, lifespan и пагинацию.
3. `app/server/core/router.py` подключает API-роутер с префиксом `/api`.
4. Роуты модуля `users` принимают входные параметры и вызывают `UserService`.
5. Сервис выполняет бизнес-логику, бросает `BackendException` при доменных
   ошибках и возвращает Pydantic-схемы.
6. Репозиторий работает с SQLAlchemy async-сессией и возвращает ORM-модели.
7. Ошибки централизованно конвертируются в JSON-ответы middleware/handlers.

## Основные абстракции

- `CoreModel` - базовый SQLAlchemy `DeclarativeBase` с `sid`, `created_at`,
  `updated_at` и автоматическим `__tablename__`.
- `CoreSchema` - базовая Pydantic-схема с camelCase alias generator,
  `from_attributes=True` и нормализацией `datetime`.
- `IPostgresBaseRepo` - контракт общего CRUD-репозитория PostgreSQL.
- `IRedisBaseRepository` - контракт базовых операций Redis.
- `IS3BaseRepository` - контракт базовых операций S3.
- `BackendException` - единый тип доменных API-ошибок.

## Инфраструктура

PostgreSQL используется как основное хранилище. Alembic берет metadata из
`CoreModel.metadata`; миграции лежат в `alembic/versions`.

Redis подключен как кэш/быстрое key-value хранилище. Базовая реализация
находится в `app/shared/repositories/redis/redis_base_repo.py`.

MinIO используется как S3-совместимое хранилище для файлов. Базовая реализация
находится в `app/shared/repositories/s3/s3_base_repo.py`.
