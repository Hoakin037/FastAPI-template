from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


class SQLFilterBase(Filter):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
