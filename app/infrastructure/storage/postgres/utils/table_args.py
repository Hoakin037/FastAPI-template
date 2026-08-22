from ..schemas import PostgresSchemas


def table_args(schema: PostgresSchemas, comment: str | None = None):
    comment = comment if comment else f"{schema.value} module schema"

    return {"schema": schema.value, "comment": comment}
