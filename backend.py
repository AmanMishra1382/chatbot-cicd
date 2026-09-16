from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver


# Load environment variables from .env
load_dotenv()


# Mistral LLM
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# Chat node
def chat_node(state: ChatState):

    messages = state["messages"]

    response = model.invoke(messages)

    return {
        "messages": [response]
    }


# Checkpointer
checkpointer = MemorySaver()


# Create graph
graph = StateGraph(ChatState)


# Add node
graph.add_node("chat_node", chat_node)


# Add edges
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


# Compile graph
chatbot = graph.compile(
    checkpointer=checkpointer
)


# Function that Streamlit will call
def get_response(user_input: str, thread_id: str):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    response = chatbot.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        },
        config=config
    )

    return response["messages"][-1].content