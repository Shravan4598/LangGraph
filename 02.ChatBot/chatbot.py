from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import BaseMessage,add_messages
from langchain_core.messages import HumanMessage,AIMessage
from typing import Annotated,TypedDict,Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver


load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class ChatBotState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def ChatBot_Node(state:ChatBotState)->ChatBotState:
    message=state["messages"]
    response=llm.invoke(message).content
    return {"messages":[response]}

graph=StateGraph(ChatBotState)
graph.add_node("ChatBotNode",ChatBot_Node)

graph.add_edge(START,"ChatBotNode")
graph.add_edge("ChatBotNode",END)

#workflow=graph.compile()
# initial_state={
#     "messages":"Hi"
# }
# result=workflow.invoke(initial_state)
# print(result["messages"][-1].content)


connection=sqlite3.connect(database="chatbot.db",check_same_thread=False)


checkpointer=SqliteSaver(conn=connection)

chatbot=graph.compile(checkpointer=checkpointer)


def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)

# thread_id="1"

# config={
#     "configurable":{
#         "thread_id":thread_id
#     }
# }

# while True:
#     user_input=input("User:")
#     if user_input== "quit" or user_input=="exit":
#         print("Goodbye,Take care.")
#         break
#     else:
#         initial_state={"messages":[HumanMessage(content=user_input)]}
#         result=chatbot.invoke(initial_state,config=config)
#         print("AI:",result["messages"][-1].content)