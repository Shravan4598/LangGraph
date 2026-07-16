# ==============================
# Imports
# ==============================

from typing import TypedDict, Literal
from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
# ==============================
# LLM
# ==============================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)


# ==============================
# Structured Output Schemas
# ==============================

class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(
        description="Sentiment of the customer review"
    )


class DiagnosisSchema(BaseModel):
    issue_type: Literal[
        "Bug",
        "Performance",
        "UI/UX",
        "Support",
        "Other"
    ]

    tone: Literal[
        "angry",
        "frustrated",
        "disappointed",
        "neutral"
    ]

    urgency: Literal[
        "low",
        "medium",
        "high"
    ]


# ==============================
# Structured Models
# ==============================

sentiment_model = llm.with_structured_output(SentimentSchema)
diagnosis_model = llm.with_structured_output(DiagnosisSchema)


# ==============================
# LangGraph State
# ==============================

class ReviewState(TypedDict, total=False):
    review: str
    sentiment: str
    diagnosis: dict
    response: str


# ==============================
# Node 1 : Sentiment Analysis
# ==============================

def Sentiment_Node(state: ReviewState):

    prompt = f"""
Analyze the following customer review.

Review:
{state['review']}

Return only the sentiment.
"""

    result = sentiment_model.invoke(prompt)

    return {
        "sentiment": result.sentiment
    }


# ==============================
# Router
# ==============================

def check_sentiment(
    state: ReviewState
) -> Literal["positive_response", "run_diagnosis"]:

    if state["sentiment"] == "positive":
        return "positive_response"

    return "run_diagnosis"


# ==============================
# Positive Response Node
# ==============================

def positive_response(state: ReviewState):

    prompt = f"""
A customer wrote the following positive review:

{state['review']}

Write a warm thank-you response.
"""

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }


# ==============================
# Diagnosis Node
# ==============================

def run_diagnosis(state: ReviewState):

    prompt = f"""
Analyze the following negative customer review.

Review:
{state['review']}

Identify:

1. issue_type
2. tone
3. urgency
"""

    diagnosis = diagnosis_model.invoke(prompt)

    return {
        "diagnosis": diagnosis.model_dump()
    }


# ==============================
# Negative Response Node
# ==============================

def negative_response(state: ReviewState):

    diagnosis = state["diagnosis"]

    prompt = f"""
You are a professional customer support agent.

Issue Type:
{diagnosis['issue_type']}

Tone:
{diagnosis['tone']}

Urgency:
{diagnosis['urgency']}

Customer Review:
{state['review']}

Write an empathetic support response.
"""

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }


# ==============================
# Build Graph
# ==============================

graph = StateGraph(ReviewState)

graph.add_node("Sentiment_Node", Sentiment_Node)
graph.add_node("positive_response", positive_response)
graph.add_node("run_diagnosis", run_diagnosis)
graph.add_node("negative_response", negative_response)

graph.add_edge(START, "Sentiment_Node")

graph.add_conditional_edges(
    "Sentiment_Node",
    check_sentiment
)

graph.add_edge("positive_response", END)

graph.add_edge(
    "run_diagnosis",
    "negative_response"
)

graph.add_edge(
    "negative_response",
    END
)

workflow = graph.compile()


# ==============================
# Test
# ==============================

initial_state = {
    "review": "I have been trying to log in for two days. The app crashes every time. This is very frustrating."
}

result = workflow.invoke(initial_state)

print("\nFinal Output:\n")
print(result)