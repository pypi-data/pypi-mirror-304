from abc import ABC, abstractmethod
from typing import Optional
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

class BaseChatbotBuilder(ABC):
    def __init__(
        self,
        prompt: Optional[str] = None,
        model_name: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ):
        self.model_name = model_name
        self.memory = MemorySaver()

        self.llm = ChatOpenAI(model=self.model_name, temperature=temperature, max_tokens=max_tokens)
        self.user_prompt = prompt or "Eres un asistente útil."
        self.prompt = f"{self.user_prompt}\n{{context}}"

    @abstractmethod
    def _create_agent_executor(self):
        """Crear el agente ejecutor con el modelo de lenguaje y las herramientas."""
        pass

    @abstractmethod
    def get_response(self, message: str, thread_id: str = "default") -> str:
        """Obtener una respuesta del chatbot para un mensaje dado y un ID de hilo."""
        pass

    def interactive_chat(self):
        """Iniciar una sesión de chat interactiva con el chatbot."""
        print("Iniciando sesión de chat. Escribe 'salir' para terminar.")
        while True:
            message = input("Usuario: ")
            if message.lower() == 'salir':
                print("Chat finalizado.")
                break
            response = self.get_response(message)
            print(f"Chatbot: {response}")