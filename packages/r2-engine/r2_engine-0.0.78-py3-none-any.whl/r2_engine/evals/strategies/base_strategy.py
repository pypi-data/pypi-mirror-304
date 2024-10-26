from abc import ABC, abstractmethod

class EvaluationStrategyBase(ABC):
    @abstractmethod
    def evaluate(self, chatbot, conversation_history):
        """Evaluar el chatbot basado en el historial de conversación."""
        pass
