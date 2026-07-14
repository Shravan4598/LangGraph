from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class llm_state(TypedDict):
    question:str
    answer:str

#defining node
def llm_node(state:llm_state)->llm_state:

    #Extract the question from the state
    question=state["question"]

    #Creating  prompt
    prompt=f"Answer the following question {question}"

    #get the answer fromthe llm
    response=llm.invoke(prompt)

    # update the answer
    answer=response.content

    return {
        "answer":answer
    }

# Adding node 

graph=StateGraph(llm_state)

graph.add_node("llm_node",llm_node)

# Adding Edge

graph.add_edge(START,"llm_node")
graph.add_edge("llm_node",END)

#Compilation
workflow=graph.compile()

#Input State
initial_state={
    "question":"How far is the moon from the Earth?"
}

#Result
result=workflow.invoke(initial_state)

print(result)
print("===="*10)
print(result["answer"])