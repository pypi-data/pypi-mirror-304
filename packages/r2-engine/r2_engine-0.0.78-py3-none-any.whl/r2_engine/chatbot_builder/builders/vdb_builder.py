from typing import List, Optional, Union
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FastEmbedEmbeddings
from langgraph.prebuilt import create_react_agent, ToolNode
from langchain.tools.retriever import create_retriever_tool
from r2_engine.chatbot_builder.builders import BaseChatbotBuilder
import requests
import tempfile
import os
import mimetypes

class ChatbotVDBBuilder(BaseChatbotBuilder):
    def __init__(
            self,
            knowledge_base: List[str],
            prompt: Optional[str] = None,
            tools: Optional[List] = None,
            model_name: str = "gpt-4o",
            search_k: int = 10,
    ):
        """
        Inicializa el constructor del Chatbot con una base de conocimientos obligatoria.

        Args:
            knowledge_base (List[str]): Lista de URLs o rutas a archivos locales (PDF o TXT).
            prompt (Optional[str], optional): Prompt personalizado para el modelo. Defaults to None.
            tools (Optional[List], optional): Lista de herramientas adicionales para el chatbot. Defaults to None.
            model_name (str, optional): Nombre del modelo de lenguaje a utilizar. Defaults to "gpt-4".
            search_k (int, optional): Número de resultados de búsqueda a retornar. Defaults to 10.
        """
        if not knowledge_base:
            raise ValueError("`knowledge_base` es obligatorio y no puede estar vacío.")

        super().__init__(prompt=prompt, model_name=model_name)
        self.search_k = search_k
        self.docs = []
        self.embeddings = FastEmbedEmbeddings()
        self.knowledge_base = knowledge_base

        self._load_documents(self.knowledge_base)
        self._create_vector_store()
        self._setup_tools(tools)
        self._create_agent_executor()

    def _load_documents(self, knowledge_base: List[str]):
        """
        Cargar y preprocesar documentos desde URLs o rutas locales.
        """
        for source in knowledge_base:
            try:
                if self._is_url(source):
                    print(f"Descargando documento desde URL: {source}")
                    response = requests.get(source)
                    response.raise_for_status()
                    content_type = response.headers.get('Content-Type', '')
                    extension = mimetypes.guess_extension(content_type.split(';')[0])

                    if extension != '.pdf':
                        print(f"Tipo de contenido no soportado para URL {source}: {content_type}")
                        continue

                    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
                        tmp_file.write(response.content)
                        tmp_file_path = tmp_file.name

                    loader = PyPDFLoader(tmp_file_path)
                    for page in loader.lazy_load():
                        page.metadata = {
                            'keywords': ['documento', 'texto']
                        }
                        self.docs.append(page)

                    os.remove(tmp_file_path)
                    print(f"Documento descargado y archivo temporal eliminado: {tmp_file_path}")

                elif os.path.isfile(source):
                    print(f"Cargando documento local: {source}")
                    extension = os.path.splitext(source)[1].lower()

                    if extension == '.pdf':
                        loader = PyPDFLoader(source)
                    elif extension == '.txt':
                        loader = TextLoader(source)
                    else:
                        print(f"Tipo de archivo no soportado para {source}: {extension}")
                        continue

                    for page in loader.lazy_load():
                        page.metadata = {
                            'keywords': ['documento', 'texto']
                        }
                        self.docs.append(page)

                    print(f"Documento local cargado: {source}")

                else:
                    print(f"Fuente no válida o archivo no encontrado: {source}")

            except requests.exceptions.RequestException as e:
                print(f"Error al descargar el documento desde {source}: {e}")
            except Exception as e:
                print(f"Error al procesar el documento desde {source}: {e}")

    def _is_url(self, path: str) -> bool:
        """
        Verifica si una cadena es una URL.
        """
        return path.startswith('http://') or path.startswith('https://')

    def _create_vector_store(self):
        """
        Crear un vector store a partir de los documentos cargados.
        """
        if not self.docs:
            self.vector_store = None
            print("No se cargaron documentos. Vector store no creado.")
            return

        print("Creando un nuevo vector store...")
        self.vector_store = FAISS.from_documents(self.docs, embedding=self.embeddings)
        print("Vector store creado exitosamente.")

    def _setup_tools(self, user_tools: Optional[List]):
        """
        Configurar las herramientas del retriever y otras utilidades.
        """
        default_tools = []

        if self.vector_store:
            retriever = self.vector_store.as_retriever(search_kwargs={"k": self.search_k})
            retriever_tool = create_retriever_tool(
                retriever,
                name="document_search",
                description="Busca y devuelve información relevante de los documentos proporcionados"
            )
            default_tools.append(retriever_tool)

        self.tools = default_tools

        if user_tools:
            self.tools.extend(user_tools)

        self.tool_node = ToolNode(self.tools)

    def _create_agent_executor(self):
        """
        Crear el agente ejecutor con el modelo de lenguaje y las herramientas.
        """
        self.agent_executor = create_react_agent(
            self.llm,
            tools=self.tool_node,
            checkpointer=self.memory,
            state_modifier=self.prompt
        )
        print("Agente ejecutor creado exitosamente.")

    def update_vector_store(self, new_documents: List[str]):
        """
        Actualiza el vector store agregando nuevos documentos.
        """
        if not self.vector_store:
            print("Vector store no existe. Creando uno nuevo.")
            self._load_documents(new_documents)
            self._create_vector_store()
            self._setup_tools(self.tools)
            self._create_agent_executor()
            return

        new_docs = []
        for source in new_documents:
            try:
                if self._is_url(source):
                    print(f"Descargando nuevo documento desde URL: {source}")
                    response = requests.get(source)
                    response.raise_for_status()
                    content_type = response.headers.get('Content-Type', '')
                    extension = mimetypes.guess_extension(content_type.split(';')[0])

                    if extension != '.pdf':
                        print(f"Tipo de contenido no soportado para URL {source}: {content_type}")
                        continue

                    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
                        tmp_file.write(response.content)
                        tmp_file_path = tmp_file.name

                    loader = PyPDFLoader(tmp_file_path)
                    for page in loader.lazy_load():
                        page.metadata = {
                            'keywords': ['documento', 'texto']
                        }
                        new_docs.append(page)

                    os.remove(tmp_file_path)
                    print(f"Nuevo documento descargado y archivo temporal eliminado: {tmp_file_path}")

                elif os.path.isfile(source):
                    print(f"Cargando nuevo documento local: {source}")
                    extension = os.path.splitext(source)[1].lower()

                    if extension == '.pdf':
                        loader = PyPDFLoader(source)
                    elif extension == '.txt':
                        loader = TextLoader(source)
                    else:
                        print(f"Tipo de archivo no soportado para {source}: {extension}")
                        continue

                    for page in loader.lazy_load():
                        page.metadata = {
                            'keywords': ['documento', 'texto']
                        }
                        new_docs.append(page)

                    print(f"Nuevo documento local cargado: {source}")

                else:
                    print(f"Fuente no válida o archivo no encontrado: {source}")

            except requests.exceptions.RequestException as e:
                print(f"Error al descargar el nuevo documento desde {source}: {e}")
            except Exception as e:
                print(f"Error al procesar el nuevo documento desde {source}: {e}")

        if new_docs:
            print("Añadiendo nuevos documentos al vector store existente...")
            self.vector_store.add_documents(new_docs)
            print("Nuevos documentos añadidos exitosamente al vector store.")
        else:
            print("No se añadieron nuevos documentos al vector store.")

    def get_response(self, message: str, thread_id: str = "default") -> str:
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
        response = self.agent_executor.invoke(payload, config={"thread_id": thread_id})
        
        return response["messages"][-1].content
