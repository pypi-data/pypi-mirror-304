from langchain_openai import ChatOpenAI
from langchain import hub

def answer_hallucination_evaluator(run, example) -> dict:
    """
    Evaluador para detectar alucinaciones en la respuesta
    """
    prediction = run.outputs["answer"]
    contexts = run.outputs["contexts"]

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    grade_prompt_hallucinations = hub.pull("langchain-ai/rag-answer-hallucination")
    answer_grader = grade_prompt_hallucinations | llm

    score = answer_grader.invoke({
        "documents": contexts,
        "student_answer": prediction
    })["Score"]

    return {"key": "answer_hallucination", "score": score}