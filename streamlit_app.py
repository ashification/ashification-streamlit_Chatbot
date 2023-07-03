""" File to run chat bot app"""
import os
import openai
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

#uName_Check = os.environ.get("GENAI_CHATBOT_USERNAME")
#pwd_Check = os.environ.get("GENAI_CHATBOT_PASSWORD")
#API_KEY = os.environ.get("GENAI_CHATBOT_APIKEY")


st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Hugging Face Credentials
with st.sidebar:
    st.title('Group 3 Login')
    #st.write('User:', uName_Check, 'Pass', pwd_Check)
    st.write('User: ', st.secrets['EMAIL'],'  Pass:', st.secrets['PASS'])

    if "password_correct" not in st.session_state:
        st.warning('Please enter your credentials!', icon='⚠️')
        hf_email = st.text_input('Enter E-mail:', type='password')
        hf_pass = st.text_input('Enter password:', type='password')
        st.write('User: ', hf_email,' Pass: ', hf_pass)
        button = st.button("Log in")    
        if button:
            if (hf_email == st.secrets['EMAIL']) and (hf_pass == st.secrets['PASS']):
                st.session_state["password_correct"] = True 

    else:
        st.success('Successful Login!', icon='✅')
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        button = st.button("Log Out")    
        if button:
            st.session_state["password_correct"] = False 




    


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)