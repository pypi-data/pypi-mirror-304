import streamlit as st
import streamlit.components.v1 as components
import os

def chat_input():
    path_to_html = os.path.join(os.path.dirname(__file__), 'static', 'chat.html')
    with open(path_to_html, 'r') as file:
        chat_input_html = file.read()
    components.html(chat_input_html, height=600)