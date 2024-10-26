class AutoImprover:
    def __init__(self, chatbot, evaluator, threshold: float):
        self.chatbot = chatbot
        self.evaluator = evaluator
        self.threshold = threshold
        self.parameters = {
            'temperature': chatbot.llm.temperature,
            'max_tokens': chatbot.llm.max_tokens,
        }

    def improve(self, conversation_history):
        evaluation_report = self.evaluator.evaluate(self.chatbot, conversation_history)
        if evaluation_report.get('fluency', 0) < self.threshold:
            self.parameters['temperature'] = max(0, self.parameters['temperature'] - 0.1)
            self.chatbot.llm.temperature = self.parameters['temperature']
        if evaluation_report.get('usefulness', 0) < self.threshold:
            self.parameters['max_tokens'] = min(4096, self.parameters['max_tokens'] + 50)
            self.chatbot.llm.max_tokens = self.parameters['max_tokens']
        return evaluation_report
