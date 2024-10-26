from .base_strategy import EvaluationStrategyBase
from typing import List
from langchain_openai import ChatOpenAI
import os

class AutomaticEvaluator(EvaluationStrategyBase):
    def __init__(self, threshold: float):
        self.threshold = threshold
    def evaluate(self, chatbot, conversation_history) -> dict:
        """
        Evaluar automáticamente el chatbot utilizando un LLM.

        Retorna:
            dict: Un reporte con las métricas de evaluación.
        """
        # Combinar el historial de conversación en un solo string
        conversation_text = ""
        for turn in conversation_history:
            conversation_text += f"Usuario: {turn['user']}\nAsistente: {turn['assistant']}\n"

        # Prompt para la evaluación
        prompt = f"""
        Eres un evaluador experto de asistentes virtuales. Evalúa la siguiente conversación entre un usuario y un asistente.

        Conversación:
        {conversation_text}

        Por favor, proporciona una evaluación numérica de 1 a 5 en las siguientes métricas:
        - Fluidez: ¿Qué tan clara y natural es la respuesta del asistente?
        - Utilidad: ¿La respuesta del asistente es útil y responde a la pregunta del usuario?

        Además, proporciona comentarios detallados sobre cómo el asistente puede mejorar.

        Formato de salida:
        Fluidez: [puntuación]
        Utilidad: [puntuación]
        Comentarios: [comentarios]
        """
        llm = ChatOpenAI(model="gpt-4o",
            max_tokens=500,
            temperature=0.0,)

        response = llm.invoke(prompt).content
        evaluation_report = self.parse_evaluation(response)
        return evaluation_report

    def parse_evaluation(self, evaluation_text: str) -> dict:
        """Parsear el texto de evaluación y convertirlo en un diccionario."""
        lines = evaluation_text.split('\n')
        report = {}
        for line in lines:
            if line.startswith('Fluidez:'):
                report['fluency'] = float(line.replace('Fluidez:', '').strip())
            elif line.startswith('Utilidad:'):
                report['usefulness'] = float(line.replace('Utilidad:', '').strip())
            elif line.startswith('Comentarios:'):
                report['comments'] = line.replace('Comentarios:', '').strip()
        return report
