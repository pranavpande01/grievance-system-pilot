import streamlit as st
import time
import os
import subprocess
from util2 import generate_thread_id
import redis
from backend import load_convo
MESSAGES_KEY = 'messages'
THREAD_ID="thread_id"
APP_TITLE = "Portal Pilot"
TEMP_VAR_THREADS="temp_var_threads"

##################################################################################################
# Redis Section
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
REDIS_STREAM = "to_back" 

##################################################################################################
# State Mgmt
def initialize_session_state():
    if MESSAGES_KEY and THREAD_ID and TEMP_VAR_THREADS not in st.session_state:
        st.session_state[MESSAGES_KEY] = []
        st.session_state[THREAD_ID]=generate_thread_id()
        st.session_state[TEMP_VAR_THREADS]=[st.session_state[THREAD_ID]]
        

def add_user_message(content): 
    to_send = {
        'role': 'user',
        'content': content,
        'thread_id':st.session_state[THREAD_ID]
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
    st.session_state[THREAD_ID]=generate_thread_id()
    st.session_state[TEMP_VAR_THREADS].append(st.session_state[THREAD_ID])



def display_chat_messages():
    for message in st.session_state[MESSAGES_KEY]:
        with st.chat_message(message['role']):
            st.write(message['content'])  

def setup_sidebar():
    st.sidebar.title(APP_TITLE)
    if st.sidebar.button("new chat"):
        clear_chat_history()
    for i in st.session_state[TEMP_VAR_THREADS]:
        if st.sidebar.button(i):
            st.session_state[THREAD_ID]=i
            st.session_state[MESSAGES_KEY] = load_convo(i)

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