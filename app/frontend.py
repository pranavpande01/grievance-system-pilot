import streamlit as st
import time
import os
import subprocess
from util2 import generate_thread_id
#from backend import respond
import redis
MESSAGES_KEY = 'messages'
APP_TITLE = "Portal Pilot"

##################################################################################################
# Redis Section
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
REDIS_STREAM = "to_back" 

##################################################################################################
# State Mgmt
def initialize_session_state():
    if MESSAGES_KEY not in st.session_state:
        st.session_state[MESSAGES_KEY] = []
        thread_id=generate_thread_id()

def add_user_message(content): 
    to_send = {
        'role': 'user',
        'content': content
    }    
    
    # send message
    redis_client.xadd("to_back", to_send) 
    # update state
    st.session_state[MESSAGES_KEY].append(to_send)

    # recieve response
    msg = redis_client.xread({"from_back": "$"}, block=0, count=1)[0][1][0][1]
    # update state
    st.session_state[MESSAGES_KEY].append(msg)


##################################################################################################

def clear_chat_history():
    st.session_state[MESSAGES_KEY] = []


def display_chat_messages():
    for message in st.session_state[MESSAGES_KEY]:
        with st.chat_message(message['role']):
            st.write(message['content'])  

def setup_sidebar():
    st.sidebar.title(APP_TITLE)
    
    if st.sidebar.button("new chat"):
        clear_chat_history()
##################################################################################################

def main():

    initialize_session_state()
    setup_sidebar()
    
    user_input = st.chat_input("Type here...")
    if user_input:
        add_user_message(user_input)


    display_chat_messages()

if __name__ == "__main__":
    
    if not subprocess.run(["docker","ps","--filter","publish=6379","--format","{{.ID}}"],stdout=subprocess.PIPE).stdout.strip(): os.system("docker run -d -p 6379:6379 --name langgraph-redis redis")
    main()