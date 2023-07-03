""" File to run chat bot app"""
import os
import openai
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

#uName_Check = os.environ.get("GENAI_CHATBOT_USERNAME")
#pwd_Check = os.environ.get("GENAI_CHATBOT_PASSWORD")
#API_KEY = os.environ.get("GENAI_CHATBOT_APIKEY")
#hf_email = ""
#hf_pass = ""


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Hugging Face Credentials
with st.sidebar:
    st.title('Group 3 Login')
    #st.write('User:', uName_Check, 'Pass', pwd_Check)

    if check_password():
        button = st.button("Log Out")    
        if button:
            st.session_state.usr_session = False
        st.success('Successful Login!', icon='✅')
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")


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