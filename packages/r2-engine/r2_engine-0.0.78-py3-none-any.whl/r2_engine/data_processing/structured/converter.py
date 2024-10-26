import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from typing import Optional, Dict, Any, Callable
import logging
import re
import unicodedata
import yaml

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("process_data.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Carga la configuración desde un archivo YAML.
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    logger.info(f"Configuración cargada desde '{config_path}'.")
    return config


def remove_accents(input_str: str) -> str:
    """
    Elimina los acentos de una cadena de texto.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    return only_ascii


def sanitize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de las columnas eliminando acentos y caracteres especiales.
    """
    original_columns = df.columns.tolist()
    df.columns = [
        re.sub(r'\W+', '_', remove_accents(col.strip().lower()))
        for col in df.columns
    ]
    logger.debug(f"Nombres de columnas originales: {original_columns}")
    logger.debug(f"Nombres de columnas sanitizados: {df.columns.tolist()}")
    return df


def load_google_sheet(url: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """
    Carga datos desde una hoja de Google Sheets.
    """
    logger.info(f"Cargando datos desde Google Sheets: {url}, Hoja: {sheet_name}")
    csv_export_url = convert_google_sheet_url_to_csv(url, sheet_name)
    try:
        df = pd.read_csv(csv_export_url)
        logger.info(f"Datos cargados exitosamente desde: {csv_export_url}")
        return df
    except Exception as e:
        logger.error(f"Error al cargar datos desde Google Sheets: {e}")
        raise


def convert_google_sheet_url_to_csv(url: str, sheet_name: Optional[str] = None) -> str:
    """
    Convierte una URL de Google Sheets a una URL de exportación CSV.
    """
    base_url = re.split(r'/edit.*', url)[0]
    export_url = f"{base_url}/export?format=csv"
    if sheet_name:
        encoded_sheet_name = re.sub(r'\s+', '+', sheet_name)
        export_url += f"&sheet={encoded_sheet_name}"
    return export_url


def validate_data(df: pd.DataFrame) -> None:
    """
    Valida que el DataFrame no esté vacío y no contenga filas o columnas completamente vacías.
    """
    if df.empty:
        raise ValueError("El DataFrame está vacío.")
    if df.isna().all().any():
        empty_cols = df.columns[df.isna().all()].tolist()
        raise ValueError(f"Columnas completamente vacías: {empty_cols}")
    if df.isna().all(axis=1).any():
        raise ValueError("Existen filas completamente vacías en el DataFrame.")
    logger.info("Datos validados correctamente.")


def filter_data(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
    """
    Filtra las filas donde la columna especificada no es igual al valor dado.
    """
    if column not in df.columns:
        raise ValueError(f"La columna '{column}' no existe en el DataFrame.")
    filtered_df = df[df[column] != value]
    logger.info(f"Filtrado de datos: {len(df) - len(filtered_df)} filas eliminadas.")
    return filtered_df


def load_structure_json(json_path: str) -> Dict[str, Any]:
    """
    Carga la estructura de tablas desde un archivo JSON.
    """
    import json
    with open(json_path, 'r', encoding='utf-8') as f:
        structure = json.load(f)
    logger.info(f"Estructura cargada desde '{json_path}'.")
    return structure


def map_string_to_sqlalchemy_type(type_str: str):
    """
    Mapea un string de tipo de datos a un tipo de datos de SQLAlchemy.
    """
    type_str_lower = type_str.lower()
    mapping = {
        "integer": Integer,
        "int": Integer,          # Añadido para manejar 'int'
        "string": String,
        "float": Float,
        "date": DateTime,
        "datetime": DateTime,    # Añadido para manejar 'datetime'
        "boolean": Boolean,
        "bool": Boolean          # Añadido para manejar 'bool'
    }
    if type_str_lower in mapping:
        sqlalchemy_type = mapping[type_str_lower]
    else:
        sqlalchemy_type = String
        logger.warning(f"Tipo de datos desconocido '{type_str}', usando 'String' por defecto.")
    return sqlalchemy_type


def sanitize_table_name(name: str) -> str:
    """
    Sanitiza el nombre de una tabla eliminando caracteres especiales y convirtiendo a minúsculas.
    """
    name = re.sub(r'\W+', '_', name).lower()
    return name


def create_tables(metadata: MetaData, structure: Dict[str, Any], table_prefix: str = "") -> Dict[str, Table]:
    """
    Crea tablas en el metadata según la estructura definida.
    """
    tables = {}
    for table_name, table_def in structure.get("tables", {}).items():
        sanitized_name = sanitize_table_name(table_name)
        full_table_name = f"{table_prefix}{sanitized_name}"
        logger.info(f"Definiendo tabla: {full_table_name}")

        columns = []
        for col in table_def.get("columns", []):
            col_name = col["name"]
            col_type = map_string_to_sqlalchemy_type(col["type"])
            nullable = col.get("nullable", True)
            unique = col.get("unique", False)
            if col_name == table_def.get("primary_key"):
                columns.append(Column(col_name, col_type, primary_key=True))
            elif col_name in table_def.get("foreign_keys", {}):
                ref_table, ref_column = table_def["foreign_keys"][col_name].split(".")
                ref_table_full = f"{table_prefix}{sanitize_table_name(ref_table)}"
                columns.append(Column(col_name, col_type, ForeignKey(f"{ref_table_full}.{ref_column}")))
            else:
                columns.append(Column(col_name, col_type, nullable=nullable, unique=unique))

        table = Table(full_table_name, metadata, *columns)
        tables[full_table_name] = table
    return tables


def to_sql(config: Dict[str, Any], data_processor: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None) -> None:
    """
    Procesa datos desde Google Sheets y los convierte en múltiples tablas SQL según una estructura JSON.

    :param config: Diccionario de configuración cargado desde YAML.
    :param data_processor: Función opcional para procesar el DataFrame antes de la inserción.
    """
    source = config["source"]
    db_uri = config["db_uri"]
    structure_json = config["structure_json"]
    sheet_name = config.get("sheet_name")
    table_prefix = config.get("table_prefix", "")

    engine = create_engine(db_uri)
    metadata = MetaData()

    # Cargar estructura
    structure = load_structure_json(structure_json)

    # Cargar datos
    df = load_google_sheet(source, sheet_name)

    # Sanitizar columnas
    df = sanitize_column_names(df)

    # Validar datos
    validate_data(df)

    # Procesar datos
    if data_processor:
        df = data_processor(df)

    # Crear tablas
    tables = create_tables(metadata, structure, table_prefix)

    # Crear tablas en la base de datos
    metadata.create_all(engine)
    logger.info("Tablas creadas en la base de datos.")

    # Insertar datos
    with engine.begin() as connection:
        for table_name, table in tables.items():
            table_def = structure["tables"][table_name.replace(table_prefix, "")]
            relevant_columns = [col["name"] for col in table_def["columns"]]
            missing_cols = [col for col in relevant_columns if col not in df.columns]
            if missing_cols:
                logger.warning(f"Columnas faltantes {missing_cols} para la tabla '{table_name}'. Saltando inserción.")
                continue
            table_df = df[relevant_columns].drop_duplicates()

            # Identificar columnas NOT NULL para la tabla actual
            not_null_columns = [
                col["name"] for col in table_def["columns"]
                if not col.get("nullable", True)
            ]

            if not_null_columns:
                # Filtrar filas que tienen valores NULL en columnas NOT NULL
                initial_row_count = len(table_df)
                table_df = table_df.dropna(subset=not_null_columns)
                final_row_count = len(table_df)
                dropped_rows = initial_row_count - final_row_count
                if dropped_rows > 0:
                    logger.warning(
                        f"Se eliminaron {dropped_rows} filas de la tabla '{table_name}' "
                        f"por tener valores NULL en columnas NOT NULL: {not_null_columns}"
                    )

            # Insertar datos en la tabla
            try:
                table_df.to_sql(table_name, con=connection, if_exists='append', index=False)
                logger.info(f"Datos insertados en la tabla '{table_name}'.")
            except Exception as e:
                logger.error(f"Error al insertar datos en la tabla '{table_name}': {e}")

    logger.info("Proceso de carga de datos completado exitosamente.")
