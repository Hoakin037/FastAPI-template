from .settings import PostgresSetting


def get_postgres_setting():
    return PostgresSetting.model_validate({})
