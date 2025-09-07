import streamlit as st
import time
import os
import subprocess
from backend import respond
MESSAGES_KEY = 'messages'
APP_TITLE = "Portal Pilot"

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if MESSAGES_KEY not in st.session_state:
        st.session_state[MESSAGES_KEY] = []

def clear_chat_history():
    """Clear all messages from chat history"""
    st.session_state[MESSAGES_KEY] = []

def add_user_message(content):
    """Add a user message to the chat history"""
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

def main():
    """Main application logic"""

    initialize_session_state()
    setup_sidebar()
    
    user_input = st.chat_input("Type here...")
    if user_input:
        add_user_message(user_input)
        print(respond(user_input,"1"))
        #st.rerun()

    display_chat_messages()

if __name__ == "__main__":
    
    if not subprocess.run(["docker","ps","--filter","publish=6379","--format","{{.ID}}"],stdout=subprocess.PIPE).stdout.strip(): os.system("docker run -d -p 6379:6379 --name langgraph-redis redis")
    main()