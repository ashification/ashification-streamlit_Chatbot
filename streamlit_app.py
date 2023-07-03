""" File to run chat bot app"""
import os
import openai
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

uName_Check = os.environ.get('GENAI_CHATBOT_USERNAME')
pwd_Check = os.environ.get('GENAI_CHATBOT_PASSWORD')
API_KEY = os.environ.get('GENAI_CHATBOT_APIKEY')
hf_email = ""
hf_pass = ""

st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Hugging Face Credentials
with st.sidebar:
    st.title('Group 3 Login')
    st.write('User:', uName_Check, 'Pass', pwd_Check)
       
    if (hf_email == uName_Check and hf_pass == pwd_Check):
        st.success('HuggingFace Login credentials already provided!', icon='✅')
        hf_email = uName_Check
        hf_pass = pwd_Check
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    else:
        st.warning('Please enter your credentials!', icon='⚠️')
        hf_email = st.text_input('Enter Username:', type='password')
        hf_pass = st.text_input('Enter password:', type='password')
        


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