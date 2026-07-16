from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class JokeGeneratorState(TypedDict):
    topic:str
    joke:str
    explanation:str

def JokeGeneratorNode(state:JokeGeneratorState)->JokeGeneratorState:
    topic=state["topic"]
    prompt=f"Generate a joke on the topic: {topic}"
    joke=llm.invoke(prompt).content
    return {"joke":joke}

def GenerateExplanationNode(state:JokeGeneratorState)->JokeGeneratorState:
    joke=state["joke"]
    prompt =f"Give the explanantion of the following joke \n {joke}"
    explanation=llm.invoke(prompt)
    return {"explanation":explanation}

graph=StateGraph(JokeGeneratorState)
graph.add_node("JokeGeneratorNode",JokeGeneratorNode)
graph.add_node("GenerateExplanationNode",GenerateExplanationNode)
graph.add_edge(START,"JokeGeneratorNode")
graph.add_edge("JokeGeneratorNode","GenerateExplanationNode")
graph.add_edge("GenerateExplanationNode",END)

checkpointer=InMemorySaver()
workflow=graph.compile(checkpointer=checkpointer)

initial_state={"topic":"E20 Fuel in India"}

config={"configurable":{"thread_id":"1"}}

result=workflow.invoke(initial_state,config=config)
print(result)

print("======="*10)
print(workflow.get_state(config=config))
print("======="*10)
print(list(workflow.get_state_history(config=config)))
print("======="*10)
initial_state={"topic":"Narendra Modi"}

config2={"configurable":{"thread_id":"2"}}

result1=workflow.invoke(initial_state,config=config2)
print(result1)

print("======="*10)
print(workflow.get_state(config=config2))
print("======="*10)
print(list(workflow.get_state_history(config=config2)))
print("======="*10)