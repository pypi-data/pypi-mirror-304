from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI

class AgenticRAG:
    def __init__(self, retriever, llm, tools):
        self.retriever = retriever
        self.llm = llm
        self.tools = tools

    def agent(self, question):
        # El agente decide si usar el retriever o no
        pass

    def generate(self, question, context):
        # Genera la respuesta basada en el contexto
        pass

    def run(self, question):
        # Flujo principal de Agentic RAG
        action = self.agent(question)
        if action == 'retrieve':
            documents = self.retriever.retrieve(question)
            context = "\n".join([doc.page_content for doc in documents])
        else:
            context = ""
        answer = self.generate(question, context)
        return answer

