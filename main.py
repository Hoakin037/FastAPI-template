import uvicorn

from app.config.settings import ProjectSettings

project_settings = ProjectSettings()


def run_app():
    uvicorn.run(
        "app.server.core.app:app",
        host=project_settings.HOST,
        port=project_settings.PORT,
        reload=project_settings.RELOAD,
        use_colors=True,
        log_level=project_settings.LOG_LEVEL,
    )


if __name__ == "__main__":
    run_app()
