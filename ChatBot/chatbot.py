from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import BaseMessage,add_messages
from langchain_core.messages import HumanMessage,AIMessage
from typing import Annotated,TypedDict,Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class ChatBotState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def ChatBot_Node(state:ChatBotState)->ChatBotState:
    message=state["messages"]
    response=llm.invoke(message).content
    return {"messages":response}

graph=StateGraph(ChatBotState)
graph.add_node("ChatBotNode",ChatBot_Node)

graph.add_edge(START,"ChatBotNode")
graph.add_edge("ChatBotNode",END)

workflow=graph.compile()
# initial_state={
#     "messages":"Hi"
# }
# result=workflow.invoke(initial_state)
# print(result["messages"][-1].content)

while True:
    user_input=input("User:")
    if user_input== "quit" or user_input=="exit":
        break
    else:
        initial_state={"messages":user_input}
        result=workflow.invoke(initial_state)
        print("AI:",result["messages"][-1].content)