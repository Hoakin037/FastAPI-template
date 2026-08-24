from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ValidationException
from fastapi.routing import APIRoute
from fastapi_pagination import add_pagination
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware

from app.config.settings import ProjectSettings
from app.server.core.lifespan import lifespan
from app.server.core.router import api
from app.server.middleware.exception import (
    BackendExceptionHandler,
    ExceptionMiddleware,
    TypeValueExceptionHandler,
    ValidationExceptionHandler,
)
from app.shared.errors.exception import BackendException


def custom_generate_unique_id(route: APIRoute) -> str:
    return route.name


settings = ProjectSettings()

app = FastAPI(
    debug=True,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    swagger_ui_parameters={
        "docExpansion": "none",
    },
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
    exception_handlers={
        BackendException: BackendExceptionHandler().handle,
        TypeError: TypeValueExceptionHandler.handle,
        ValidationException: ValidationExceptionHandler().handle,
        ValidationError: ValidationExceptionHandler.handle,
        RequestValidationError: ValidationExceptionHandler.handle,
    },
)


def setup_middleware():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.middleware("http")(ExceptionMiddleware())


app.include_router(api)
setup_middleware()
add_pagination(app)
