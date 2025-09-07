import streamlit as st

#########################################################
if 'messages' not in  st.session_state:
    st.session_state['messages']=[]

#########################################################

st.sidebar.title("portal pilot")
if st.sidebar.button("new chat",disabled=not st.session_state['messages']):
    st.session_state['messages']=[]
    st.rerun()

if user_input:=st.chat_input():
    st.session_state['messages'].append(
        {
            'role':'user',
            'content':user_input
        }
    )
    st.rerun()
for i in st.session_state['messages']:
    with st.chat_message(i['role']):
        st.text(i['content'])

