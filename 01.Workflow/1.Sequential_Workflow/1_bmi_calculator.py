from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from IPython.display import Image,display

class bmi_state(TypedDict):
    weight_kg:float
    height_m:float
    bmi_cal:float

def bmi_node(state:bmi_state):
    weight=state["weight_kg"]
    height=state["height_m"]
    bmi= weight/(height**2)
    return {"bmi_cal":bmi}

graph=StateGraph(bmi_state)
graph.add_node("bmi_node",bmi_node)
graph.add_edge(START,"bmi_node")
graph.add_edge("bmi_node",END)

app=graph.compile()

intial_state={
    "weight_kg":80,
    "height_m":1.65
}

result=app.invoke(intial_state)
print(result)

display(app.get_graph().draw_mermaid_png())

