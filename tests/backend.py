from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.redis import RedisSaver  
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv
import redis
##################################################################################################
# REDIS SECTION
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
##################################################################################################
# LLM Section
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")
##################################################################################################
# Langgraph Section
class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# Define nodes
def chat_node(state: ChatState):
    return {
        'messages': llm.invoke(state['messages']) 
    }

checkpointer = RedisSaver(
    redis_url="redis://localhost:6379",  
)
# Define graph
graph = StateGraph(ChatState)

# Add nodes
graph.add_node("chat_node", chat_node)

# Add edges
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile chatbot
chatbot = graph.compile(checkpointer=checkpointer)

##################################################################################################
# Inference Section 
def respond(user_input):
    config = {
        "configurable": {
            "thread_id": 1
        }
    }
    print(chatbot.checkpointer)
    return chatbot.invoke(
        {'messages': [HumanMessage(content=user_input)]},
        config=config
    )['messages'][-1].content

while True:
    msg = r.xread({"to_back": "$"}, block=0, count=1)
    
    message = {
        'role': 'assistant',
        'content': respond(msg[0][1][0][1]['content'])
    }

    r.xadd("from_back", message)

