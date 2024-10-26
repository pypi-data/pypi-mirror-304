from langchain_openai import ChatOpenAI
from langchain import hub

def docs_relevance_evaluator(run, example) -> dict:
    """
    Evaluador para la relevancia de los documentos recuperados
    """
    input_question = example.inputs["input_question"]
    contexts = run.outputs["contexts"]

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    grade_prompt_doc_relevance = hub.pull("langchain-ai/rag-document-relevance")
    answer_grader = grade_prompt_doc_relevance | llm

    score = answer_grader.invoke({
        "question": input_question,
        "documents": contexts
    })["Score"]

    return {"key": "document_relevance", "score": score}