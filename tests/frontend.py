import streamlit as st
import time
import os
import subprocess
#from backend import respond
import redis
MESSAGES_KEY = 'messages'
APP_TITLE = "Portal Pilot"

##################################################################################################
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
REDIS_STREAM = "chat_stream" 

def initialize_session_state():
    if MESSAGES_KEY not in st.session_state:
        st.session_state[MESSAGES_KEY] = []
##################################################################################################

def clear_chat_history():
    st.session_state[MESSAGES_KEY] = []

def add_user_message(content):
    message = {
        'role': 'user',
        'content': content
    }
    st.session_state[MESSAGES_KEY].append(message)

def display_chat_messages():
    """Display all messages in the chat history"""
    for message in st.session_state[MESSAGES_KEY]:
        with st.chat_message(message['role']):
            st.write(message['content'])  

def setup_sidebar():
    """Setup the sidebar with controls"""
    st.sidebar.title(APP_TITLE)
    
    if st.sidebar.button("new chat"):
        clear_chat_history()
        #st.rerun()
##################################################################################################

def main():
    """Main application logic"""

    initialize_session_state()
    setup_sidebar()
    
    user_input = st.chat_input("Type here...")
    if user_input:
        add_user_message(user_input)
        redis_client.xadd(REDIS_STREAM, {"user_input": user_input})  # NEW

        #print(respond(user_input,"1"))
        #st.rerun()

    display_chat_messages()

if __name__ == "__main__":
    
    if not subprocess.run(["docker","ps","--filter","publish=6379","--format","{{.ID}}"],stdout=subprocess.PIPE).stdout.strip(): os.system("docker run -d -p 6379:6379 --name langgraph-redis redis")
    #subprocess.Popen(["python", "util.py"])
    main()