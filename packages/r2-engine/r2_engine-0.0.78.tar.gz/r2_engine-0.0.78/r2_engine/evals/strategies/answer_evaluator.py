from langchain import hub
from langchain_openai import ChatOpenAI

grade_prompt_answer_accuracy = prompt = hub.pull("langchain-ai/rag-answer-vs-reference")

def answer_evaluator(run, example) -> dict:
    """
    Un evaluador simple para la precisión de respuestas RAG
    """

    input_question = example.inputs["input_question"]  
    reference = example.outputs["output_answer"]     
    prediction = run

    # LLM grader
    llm = ChatOpenAI(model="gpt-4o", temperature=0)  

    # Prompt estructurado
    answer_grader = grade_prompt_answer_accuracy | llm

    # Ejecutar el evaluador
    score = answer_grader.invoke({
        "question": input_question,
        "correct_answer": reference,
        "student_answer": prediction
    })
    score = score["Score"]

    return {"key": "answer_v_reference_score", "score": score}
