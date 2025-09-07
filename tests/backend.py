from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
load_dotenv()

llm=ChatGoogleGenerativeAI(
    model='gemini-2.0-flash-lite'
)

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

initial_state = ChatState({
    'messages': [HumanMessage(content="Hello!")]
})

print(initial_state)
