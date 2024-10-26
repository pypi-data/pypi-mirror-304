from abc import ABC, abstractmethod

class BaseRAGStrategy(ABC):
    @abstractmethod
    def run(self, question: str) -> str:
        """Ejecutar la estrategia RAG y devolver la respuesta."""
        pass
