from .base_strategy import EvaluationStrategyBase

class ManualEvaluator(EvaluationStrategyBase):
    def __init__(self):
        pass

    def evaluate(self, chatbot, conversation_history) -> dict:
        """
        Evaluación manual del chatbot.

        Retorna:
            dict: Un reporte con las métricas de evaluación.
        """
        # Mostrar la conversación al evaluador humano
        print("Por favor, evalúa la siguiente conversación:")
        for turn in conversation_history:
            print(f"Usuario: {turn['user']}")
            print(f"Asistente: {turn['assistant']}\n")

        # Solicitar las puntuaciones al evaluador
        fluency = float(input("Puntuación de Fluidez (1-5): "))
        usefulness = float(input("Puntuación de Utilidad (1-5): "))
        comments = input("Comentarios adicionales: ")

        evaluation_report = {
            'fluency': fluency,
            'usefulness': usefulness,
            'comments': comments
        }
        return evaluation_report
