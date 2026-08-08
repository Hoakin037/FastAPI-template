from .settings import PostgresSettings


def get_postgres_setting():
    return PostgresSettings.model_validate({})
