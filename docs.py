import os
import base64
import re
import json
import requests
import streamlit as st
import openai
import time

logo = 'https://nveil.ai/wp-content/uploads/2024/07/sourcee-logo-v2.png'


st.logo(logo)


prompts, tipstricks , faq = st.tabs(["Example Prompts", "Tips & Tricks", "FAQ"])

with prompts:
    st.title("Example Prompts")
    st.write("Here are some example prompts to get you started:")
    #create a dropdown menu
    prompt = st.selectbox("Select a prompt:", ["Prompt 1", "Prompt 2", "Prompt 3"])
    if prompt == "Prompt 1":
        st.write("Prompt 1: Write a short story about a robot that becomes self-aware and tries to escape from a lab.")
    elif prompt == "Prompt 2":
        st.write("Prompt 2: Write a poem about the beauty of nature.")
    elif prompt == "Prompt 3":
        st.write("Prompt 3: Write a dialogue between two characters who are stranded on a deserted island.")

with tipstricks:
    st.title("Tips & Tricks")
    st.write("Here are some tips and tricks to help you get the most out of Sourcee:")

with faq:
    st.title("Freqently Asked Questions")
    st.write("Here are some frequently asked questions:")
    