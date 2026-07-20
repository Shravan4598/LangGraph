from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class ParentState(TypedDict):
    question:str
    eng_answer:str
    hin_answer:str


def generate_hindi(state:ParentState)->ParentState:
    prompt=f"""
    Generate the following text into hindi 
    {state["eng_answer"]}
    and do not add extra thing into it
"""
    hindi_text=llm.invoke(prompt).content
    return {"hin_answer":hindi_text}

substate=StateGraph(ParentState)
substate.add_node("generate_hindi",generate_hindi)
substate.add_edge(START,"generate_hindi")
substate.add_edge("generate_hindi",END)

subgraph=substate.compile()

def generate_answer(state:ParentState)->ParentState:
    question=state["question"]
    prompt=f"""
    Generate a answer on the question {question}
"""
    eng_answer=llm.invoke(prompt).content
    return {"eng_answer":eng_answer}

graph=StateGraph(ParentState)
graph.add_node("generate_answer",generate_answer)
graph.add_node("generate_hindi",subgraph)

graph.add_edge(START,"generate_answer")
graph.add_edge("generate_answer","generate_hindi")
graph.add_edge("generate_hindi",END)

workflow=graph.compile()
initial_state={
    "question":"What is Artificial Intelligence?"
}

result=workflow.invoke(initial_state)
print(result)