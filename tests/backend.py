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
        'messages': llm.invoke(state['messages'])

    }

#define memory
checkpointer=InMemorySaver()

#define graph
graph=StateGraph(ChatState)

#define nodes
graph.add_node("chat_node",chat_node)

#define edges
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot=graph.compile(checkpointer=checkpointer)
def respond(user_input,thread_id):
    config = {
    "configurable": {
        "thread_id": str(thread_id)
    }
    }

    return chatbot.invoke(
        {'messages':[HumanMessage(content=user_input)]},
        config=config
    )['messages'][-1].content

    