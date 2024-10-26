from sqlalchemy import create_engine, inspect
from typing import Dict, Any

def get_schema(db_uri: str) -> Dict[str, Any]:
    """
    Obtiene el esquema de la base de datos especificada.

    :param db_uri: URI de la base de datos SQL.
    :return: Diccionario que representa el esquema de la base de datos.
    """
    engine = create_engine(db_uri)
    inspector = inspect(engine)
    schema = {}

    for table_name in inspector.get_table_names():
        columns = []
        for column in inspector.get_columns(table_name):
            columns.append({
                "name": column['name'],
                "type": str(column['type']),
                "nullable": column['nullable'],
                "default": column['default']
            })
        foreign_keys = []
        for fk in inspector.get_foreign_keys(table_name):
            foreign_keys.append({
                "constrained_columns": fk['constrained_columns'],
                "referred_table": fk['referred_table'],
                "referred_columns": fk['referred_columns']
            })
        schema[table_name] = {
            "columns": columns,
            "foreign_keys": foreign_keys
        }

    return schema
