from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")

class ChatState(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]

#define nodes
def chat_node(state:ChatState):
    return {
        'message': llm.invoke(state['messages'])

    }

#define memory
checkpointer=InMemorySaver()

#define graph
graph=StateGraph(ChatState)
chatbot=graph.compile(checkpointer=checkpointer)

