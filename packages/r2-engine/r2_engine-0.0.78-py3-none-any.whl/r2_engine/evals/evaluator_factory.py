from typing import Optional
from .strategies.automatic_evaluator import AutomaticEvaluator
from .strategies.manual_evaluator import ManualEvaluator

class EvaluatorFactory:
    @staticmethod
    def get_evaluator(evaluator_type: str, **kwargs):
        if evaluator_type == 'automatic':
            threshold = kwargs.get('threshold', 0.7)
            return AutomaticEvaluator(threshold)
        elif evaluator_type == 'manual':
            return ManualEvaluator()
        else:
            raise ValueError(f"Tipo de evaluador desconocido: {evaluator_type}")
