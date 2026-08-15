from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.config.settings import ProjectSettings
from app.server.core.lifespan import lifespan
from app.server.core.router import api


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
)


app.include_router(api)
