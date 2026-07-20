from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class translate_substate(TypedDict):
    input_text:str
    translated_text:str

def substate_node(state:translate_substate)->translate_substate:
    prompt=f"Translate the follwing text into hindi and do not add extra thing keep it as it is {state["input_text"]}"
    response=llm.invoke(prompt).content
    return {"translated_text":response}

substate=StateGraph(translate_substate)
substate.add_node("substate_node",substate_node)
substate.add_edge(START,"substate_node")
substate.add_edge("substate_node",END)

subgraph=substate.compile()


class parent_state(TypedDict):
    topic:str
    generate_text:str
    hindi_text:str


def generate_text_node(state:parent_state)->parent_state:
    prompt=f"Generate a brief answer on the question {state["topic"]}"
    generate_text=llm.invoke(prompt).content
    return {"generate_text":generate_text}

def translate_text_node(state:parent_state):
    generate_text=state["generate_text"]
    x=subgraph.invoke({"input_text":generate_text})
    hindi_text=x["translated_text"]
    return {"hindi_text":hindi_text}

states=StateGraph(parent_state)
states.add_node("generate_text_node",generate_text_node)
states.add_node("translate_text_node",translate_text_node)

states.add_edge(START,"generate_text_node")
states.add_edge("generate_text_node","translate_text_node")
states.add_edge("translate_text_node",END)

graph=states.compile()

initial_state={
    "topic":"What is Artificial Intelligence?"
}


result=graph.invoke(initial_state)
print(result["hindi_text"])