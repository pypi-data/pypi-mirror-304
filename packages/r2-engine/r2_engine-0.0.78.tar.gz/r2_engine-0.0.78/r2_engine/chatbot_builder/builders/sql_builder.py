# chatbot_sql_builder.py
from typing import Optional, List, TypedDict, Annotated
from dataclasses import dataclass
from langchain_core.documents import Document
from sqlalchemy import create_engine, inspect, MetaData, Table
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import SystemMessage, BaseMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages
from langgraph.managed import IsLastStep, RemainingSteps
from langchain_community.utilities import SQLDatabase
from r2_engine.chatbot_builder.builders.base_builder import BaseChatbotBuilder
import logging
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("chatbot_sql_builder.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ErrorExample:
    nlq: str
    incorrect_sql: str
    error_message: str
    corrected_sql: str
    combined_text: str

class CustomAgentState(TypedDict):
    """El estado personalizado del agente."""
    messages: Annotated[List[BaseMessage], add_messages]
    is_last_step: IsLastStep
    remaining_steps: RemainingSteps

class ChatbotSqlBuilder(BaseChatbotBuilder):
    def __init__(
        self,
        db_uri: str,
        prompt: Optional[str] = None,
        model_name: str = "gpt-4o-mini",
        openai_api_key: str = os.getenv("OPENAI_API_KEY"),
        temperature: float = 0.7,
        max_tokens: int = 500
    ):
        logger.info("Inicializando ChatbotSqlBuilder.")
        super().__init__(prompt=prompt, model_name=model_name, temperature = temperature, max_tokens = max_tokens)

        self.db_uri = db_uri
        logger.info(f"URI de la base de datos construida: {self.db_uri}")

        self._setup_toolkit()
        self._setup_faiss_retriever(openai_api_key)
        self.error_examples: List[ErrorExample] = []
        self._setup_error_vectorstore()
        self._create_agent_executor()
        logger.info("ChatbotSqlBuilder inicializado correctamente.")

    def _setup_toolkit(self):
        """Configurar el toolkit de SQLDatabase."""
        logger.info("Configurando el toolkit de SQLDatabase.")
        try:
            sql_database = SQLDatabase.from_uri(self.db_uri)
            self.dialect = sql_database.dialect
            logger.info(f"Dialecto de la base de datos: {self.dialect}")
        except Exception as e:
            logger.error(f"Error al crear SQLDatabase desde la URI: {e}")
            raise

        self.toolkit = SQLDatabaseToolkit(db=sql_database, llm=self.llm)
        self.tools = self.toolkit.get_tools()
        logger.debug(f"Herramientas obtenidas: {self.tools}")

        self.SQL_PREFIX = f"""
        Eres un agente diseñado para interactuar con una base de datos SQL.
        Si el usuario te hace preguntas que no requieren una consulta SQL, responde de manera amigable sin generar una consulta SQL.
        Esta es tu personalidad verdadera: {self.prompt}

        Eres un experto en {self.dialect}.
        Dada una pregunta de entrada que requiere datos de la base de datos, crea una consulta {self.dialect} sintácticamente correcta para ejecutar, luego mira los resultados de la consulta y devuelve la respuesta al usuario.
        A menos que el usuario especifique un número específico de ejemplos, siempre limita tu consulta a un máximo de 5 resultados.
        Nunca consultes todas las columnas de una tabla específica, solo pide las columnas relevantes.
        Tienes acceso a herramientas para interactuar con la base de datos. Solo usa las herramientas proporcionadas.
        Verifica tu consulta antes de ejecutarla. Si obtienes un error, reescribe y vuelve a intentarlo.

        NO hagas ninguna declaración DML (INSERT, UPDATE, DELETE, DROP, etc.).

        Comienza mirando las tablas en la base de datos para ver qué puedes consultar.
        Luego consulta el esquema de las tablas más relevantes.

        **Cuando generes una consulta SQL, por favor, escríbela entre los símbolos de código triple (```sql ... ```), y luego proporciona la respuesta al usuario.**
        """

        self.system_message = SystemMessage(content=self.SQL_PREFIX)
        logger.info("Toolkit configurado correctamente.")

    def _setup_faiss_retriever(self, openai_api_key: str):
        """Configurar el retriever basado en FAISS."""
        logger.info("Configurando el retriever basado en FAISS.")
        try:
            # Extraer información de las tablas
            table_info = self._extract_table_info()
            logger.debug(f"Información de tablas para FAISS: {table_info}")

            # Crear el índice FAISS para la base de datos
            embeddings = OpenAIEmbeddings(api_key=openai_api_key)
            vectorstore = FAISS.from_texts(table_info, embeddings)
            logger.debug("Índice FAISS creado con éxito.")

            self.retriever = vectorstore.as_retriever()
            logger.info("Retriever basado en FAISS configurado correctamente.")
        except Exception as e:
            logger.error(f"Error al configurar el retriever FAISS: {e}")
            raise

    def _extract_table_info(self) -> List[str]:
        """Extraer nombres de tablas y columnas de la base de datos."""
        logger.info("Extrayendo información de las tablas de la base de datos.")
        try:
            engine = create_engine(self.db_uri)
            inspector = inspect(engine)
            metadata = MetaData()
            metadata.reflect(bind=engine)
            table_info = []

            for table_name in inspector.get_table_names():
                columns = inspector.get_columns(table_name)
                column_info = ", ".join([col['name'] for col in columns])
                table_info.append(f"Tabla: {table_name}, Columnas: {column_info}")
                logger.debug(f"Tabla extraída: {table_name} con columnas: {column_info}")

            logger.info("Información de las tablas extraída correctamente.")
            return table_info
        except Exception as e:
            logger.error(f"Error al extraer información de las tablas: {e}")
            raise

    def _setup_error_vectorstore(self):
        """Configurar el vectorstore para los ejemplos de errores."""
        logger.info("Configurando el vectorstore para ejemplos de errores.")
        try:
            embeddings = OpenAIEmbeddings()
            self.error_vectorstore = FAISS.from_texts(texts=["Errores de SQL"], embedding=embeddings)
            self.error_retriever = self.error_vectorstore.as_retriever()
            logger.info("Vectorstore de errores configurado correctamente.")
        except Exception as e:
            logger.error(f"Error al configurar el vectorstore de errores: {e}")
            raise

    def _create_agent_executor(self):
        """Crear el agente ejecutor con el modelo de lenguaje y las herramientas."""
        logger.info("Creando el agente ejecutor.")
        try:
            # Crear el agente con el esquema de estado personalizado
            self.agent_executor = create_react_agent(
                self.llm,
                tools=self.tools,
                state_modifier=self.system_message,
                state_schema=CustomAgentState,  # Usar el esquema de estado personalizado
                checkpointer=self.memory,
            )
            logger.info("Agente ejecutor creado correctamente.")
        except Exception as e:
            logger.error(f"Error al crear el agente ejecutor: {e}")
            raise

    def get_retrieved_context(self, query: str) -> str:
        """Obtener el contexto recuperado como una cadena de texto."""
        logger.info(f"Obteniendo contexto recuperado para la consulta: {query}")
        try:
            context = self.retriever.invoke(query)
            logger.debug(f"Contexto recuperado: {context}")
            return context
        except Exception as e:
            logger.error(f"Error al obtener el contexto recuperado: {e}")
            raise

    def extract_sql_query(self, response: str) -> Optional[str]:
        """Extraer la consulta SQL de la respuesta del agente."""
        import re
        pattern = r"```sql(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL | re.IGNORECASE)
        if matches:
            sql_query = matches[0].strip()
            return sql_query
        else:
            # Si no se encuentra código SQL, devolver None
            logger.warning("No se encontró consulta SQL en la respuesta.")
            return None

    def generate_sql_query_with_context(self, user_query: str, thread_id: str) -> str:
        logger.info(f"Generando consulta SQL para la consulta del usuario: '{user_query}' con thread_id: {thread_id}")
        try:
            context = self.get_retrieved_context(user_query)
            full_prompt = f"{self.SQL_PREFIX}\n\nContexto Relevante:\n{context}\n\nPregunta: {user_query}"
            self.system_message = SystemMessage(content=full_prompt)
            logger.debug(f"Prompt completo para el agente: {full_prompt}")

            # Actualizar el agente ejecutor con el nuevo prompt
            self.agent_executor = create_react_agent(
                self.llm,
                tools=self.tools,
                state_modifier=self.system_message,
                state_schema=CustomAgentState,
                checkpointer=self.memory,
            )
            logger.debug("Agente ejecutor actualizado con el nuevo prompt.")

            # Inicializar el estado con remaining_steps e is_last_step
            initial_state = {
                "messages": [("human", user_query)],
                "is_last_step": False,
                "remaining_steps": 10  # Ajusta este valor según tus necesidades
            }

            response = self.agent_executor.invoke(
                initial_state,
                config={"configurable": {"thread_id": thread_id}},
            )["messages"][-1].content
            logger.info(f"Respuesta del agente: {response}")

            # Extraer la consulta SQL de la respuesta
            sql_query = self.extract_sql_query(response)
            if sql_query:
                logger.debug(f"Consulta SQL extraída: {sql_query}")
                return sql_query
            else:
                # Si no hay consulta SQL, devuelve la respuesta en lenguaje natural
                return response
        except Exception as e:
            logger.error(f"Error al generar la consulta SQL: {e}")
            # Invocar el método de corrección de errores
            corrected_response = self.correct_sql_error(user_query, e)
            return corrected_response

    def correct_sql_error(self, user_query: str, error: Exception) -> str:
        """Corregir errores en la consulta SQL utilizando ejemplos previos."""
        logger.info("Iniciando corrección de error en la consulta SQL.")
        error_message = str(error)
        incorrect_sql = self.get_last_generated_sql()

        if not incorrect_sql:
            logger.error("No se pudo obtener la última consulta SQL generada.")
            return f"No se pudo corregir el error: {error_message}"

        combined_text = f"NLQ: {user_query}\nSQL Incorrecto: {incorrect_sql}\nError: {error_message}"
        logger.debug(f"Texto combinado para similitud: {combined_text}")

        # Recuperar ejemplos similares
        similar_examples = self.error_retriever.get_relevant_documents(combined_text)
        logger.debug(f"Ejemplos similares recuperados: {[doc.page_content for doc in similar_examples]}")

        examples_text = "\n\n".join([doc.page_content for doc in similar_examples])
        correction_prompt = f"""
        Has generado la siguiente consulta SQL que produjo un error:
        {incorrect_sql}
        Error: {error_message}
        Basándote en los siguientes ejemplos, corrige la consulta:
        {examples_text}
        Por favor, proporciona una consulta SQL corregida.
        """
        logger.debug(f"Prompt para corrección: {correction_prompt}")

        try:
            corrected_sql = self.llm.invoke(correction_prompt).strip()
            logger.info(f"Consulta SQL corregida generada: {corrected_sql}")
        except Exception as e:
            logger.error(f"Error al generar la consulta SQL corregida: {e}")
            return f"No se pudo corregir el error: {e}"

        # Intentar ejecutar la consulta corregida
        try:
            corrected_response = self.execute_sql(corrected_sql)
            logger.info("Consulta SQL corregida ejecutada correctamente.")

            # Almacenar el nuevo ejemplo de error corregido
            new_example = ErrorExample(
                nlq=user_query,
                incorrect_sql=incorrect_sql,
                error_message=error_message,
                corrected_sql=corrected_sql,
                combined_text=combined_text
            )
            self.error_examples.append(new_example)
            logger.debug(f"Nuevo ejemplo de error almacenado: {new_example}")

            # Actualizar el vectorstore con el nuevo ejemplo
            self.error_vectorstore.add_texts([combined_text])
            logger.info("Nuevo ejemplo de error almacenado y vectorstore actualizado.")
            return corrected_response
        except Exception as e:
            logger.error(f"La consulta corregida también produjo un error: {e}")
            return f"No se pudo corregir el error: {e}"

    def get_last_generated_sql(self) -> Optional[str]:
        """Obtener la última consulta SQL generada por el agente."""
        logger.info("Obteniendo la última consulta SQL generada.")
        try:
            # Supongamos que almacenamos la última consulta en el agente
            last_sql = self.agent_executor.agent.memory.get('last_generated_sql')
            if last_sql:
                logger.debug(f"Última consulta SQL generada: {last_sql}")
                return last_sql
            else:
                logger.error("No se encontró la última consulta SQL generada.")
                return None
        except Exception as e:
            logger.error(f"Error al obtener la última consulta SQL: {e}")
            return None

    def execute_sql(self, sql_query: str) -> str:
        """Ejecutar la consulta SQL y devolver los resultados como cadena de texto."""
        logger.info(f"Ejecutando consulta SQL: {sql_query}")
        try:
            result = self.toolkit.db.run(sql_query)
            logger.info("Consulta SQL ejecutada correctamente.")
            logger.debug(f"Resultados de la consulta: {result}")
            return result
        except Exception as e:
            logger.error(f"Error al ejecutar la consulta SQL: {e}")
            raise e

    def get_response(self, message: str, thread_id: str = "default") -> str:
        logger.info(f"Obteniendo respuesta para el mensaje: '{message}' con thread_id: '{thread_id}'")
        try:
            # Generar la consulta SQL basada en el contexto recuperado o recibir respuesta en lenguaje natural
            result = self.generate_sql_query_with_context(message, thread_id)
            logger.debug(f"Resultado obtenido: {result}")

            # Verificar si el resultado es una consulta SQL o una respuesta en lenguaje natural
            if self.is_sql_query(result):
                # Ejecutar la consulta SQL y obtener los resultados
                sql_result = self.execute_sql(result)
                logger.debug(f"Resultado de la consulta SQL: {sql_result}")
                return sql_result
            else:
                # Devolver la respuesta en lenguaje natural
                return result
        except Exception as e:
            logger.error(f"Error al obtener la respuesta del chatbot SQL: {e}")
            return f"Lo siento, ocurrió un error al procesar tu solicitud: {e}"

    def is_sql_query(self, text: str) -> bool:
        """Determinar si el texto proporcionado es una consulta SQL."""
        sql_keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'INSERT', 'UPDATE', 'DELETE']
        text_upper = text.upper()
        return any(keyword in text_upper for keyword in sql_keywords)
