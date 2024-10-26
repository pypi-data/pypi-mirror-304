import pandas as pd
from typing import Optional, Dict, Any, Union
import json
import logging
import re

from langchain_openai import OpenAI

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_data(df: pd.DataFrame) -> None:
    """
    Valida que el DataFrame cumpla con ciertos criterios antes de convertirlo a una tabla SQL.

    :param df: DataFrame de pandas a validar.
    :raises ValueError: Si los datos no cumplen con los criterios.
    """
    if df.empty:
        raise ValueError("El DataFrame está vacío.")

    # Validar que no haya columnas completamente vacías
    empty_columns = df.columns[df.isna().all()].tolist()
    if empty_columns:
        raise ValueError(f"Las siguientes columnas están completamente vacías: {empty_columns}")

    # Validar que no haya filas completamente vacías
    empty_rows = df[df.isna().all(axis=1)]
    if not empty_rows.empty:
        raise ValueError("Existen filas completamente vacías en el DataFrame.")

    # Puedes agregar más validaciones según tus necesidades


def generate_table_prompt(df: pd.DataFrame) -> str:
    """
    Genera un prompt para un generador de tablas basado en IA utilizando el DataFrame proporcionado.

    :param df: DataFrame de pandas con los datos.
    :return: Prompt generado.
    """

    # Prompt para el Generador de Tablas Basado en IA
    AI_TABLE_GENERATION_PROMPT = """
    Eres un asistente experto en diseño de bases de datos SQL. A continuación, te proporciono una muestra de datos de un conjunto de datos. Por favor, genera una estructura JSON que describa las tablas necesarias para estos datos. La estructura debe seguir este formato:

    {
        "tables": {
            "nombre_tabla": {
                "columns": [
                    {"name": "id", "type": "integer", "nullable": False, "unique": True},
                    {"name": "nombre", "type": "string", "nullable": False},
                    {"name": "precio", "type": "float", "nullable": True}
                ],
                "primary_key": "id",
                "foreign_keys": {
                    "otra_tabla_id": "otra_tabla.id"
                }
            },
            "otra_tabla": {
                "columns": [
                    {"name": "id", "type": "integer", "nullable": False, "unique": True},
                    {"name": "descripcion", "type": "string", "nullable": False}
                ],
                "primary_key": "id",
                "foreign_keys": {}
            }
        }
    }

    Asegúrate de que la estructura JSON sea válida y siga este formato.

    Muestra de datos:
    {sample_data}

    Por favor, proporciona la estructura JSON para crear las tablas.
    """
    sample_data = df.head(5).to_dict(orient='records')
    sample_data_str = json.dumps(sample_data, indent=2, ensure_ascii=False)
    prompt = AI_TABLE_GENERATION_PROMPT.format(sample_data=sample_data_str)
    return prompt


def load_structure_json(json_path: str) -> Dict[str, Any]:
    """
    Carga la estructura de tablas desde un archivo JSON.

    :param json_path: Ruta al archivo JSON que define la estructura de las tablas.
    :return: Diccionario con la estructura de las tablas.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            structure = json.load(f)
        logger.info(f"Estructura JSON cargada desde '{json_path}'.")
        return structure
    except Exception as e:
        logger.error(f"Error al cargar el archivo JSON de estructura: {e}")
        raise


def send_to_llm(prompt: str) -> str:
    """
    Envía un prompt a un modelo de lenguaje y obtiene la respuesta.

    :param prompt: Texto del prompt para enviar al modelo.
    :return: Respuesta del modelo de lenguaje.
    """
    import openai
    import os

    if not openai.api_key:
        raise ValueError("La clave de API de OpenAI no está configurada en las variables de entorno.")
    llm = OpenAI(model = "gpt-4o-mini")
    try:
        response = llm.invoke({"prompt": prompt})
        return response
    except Exception as e:
        logger.error(f"Error al comunicarse con la API de OpenAI: {e}")
        raise


def extract_json_from_string(text: str) -> str:
    """
    Extrae la primera ocurrencia de un JSON válido dentro de una cadena de texto.

    :param text: Texto que contiene el JSON.
    :return: Cadena con el JSON extraído.
    :raises ValueError: Si no se encuentra un JSON válido.
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            # Verificar si es un JSON válido
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            raise ValueError("El texto extraído no es un JSON válido.")
    else:
        raise ValueError("No se encontró un JSON válido en el texto proporcionado.")


def validate_generated_structure(structure: Dict[str, Any]) -> None:
    """
    Valida que la estructura generada por la IA siga el formato esperado.

    :param structure: Diccionario que representa la estructura generada.
    :raises ValueError: Si la estructura no cumple con el formato esperado.
    """
    if "tables" not in structure:
        raise ValueError("La estructura JSON debe contener la clave 'tables'.")

    if not isinstance(structure["tables"], dict):
        raise ValueError("La clave 'tables' debe ser un diccionario.")

    for table_name, table_def in structure["tables"].items():
        if "columns" not in table_def:
            raise ValueError(f"La tabla '{table_name}' debe contener la clave 'columns'.")
        if "primary_key" not in table_def:
            raise ValueError(f"La tabla '{table_name}' debe contener la clave 'primary_key'.")
        if "foreign_keys" not in table_def:
            raise ValueError(f"La tabla '{table_name}' debe contener la clave 'foreign_keys'.")

        if not isinstance(table_def["columns"], list):
            raise ValueError(f"La clave 'columns' en la tabla '{table_name}' debe ser una lista.")
        if not isinstance(table_def["foreign_keys"], dict):
            raise ValueError(f"La clave 'foreign_keys' en la tabla '{table_name}' debe ser un diccionario.")

        for column in table_def["columns"]:
            if not all(k in column for k in ("name", "type", "nullable", "unique")):
                raise ValueError(
                    f"Cada columna en la tabla '{table_name}' debe contener 'name', 'type', 'nullable' y 'unique'.")


def extract_and_validate_json(text: str) -> Dict[str, Any]:
    """
    Extrae y valida un JSON de la cadena de texto proporcionada.

    :param text: Texto que contiene el JSON.
    :return: Diccionario con el JSON extraído y validado.
    :raises ValueError: Si no se encuentra un JSON válido o si la estructura no es correcta.
    """
    json_str = extract_json_from_string(text)
    structure = json.loads(json_str)
    validate_generated_structure(structure)
    return structure
