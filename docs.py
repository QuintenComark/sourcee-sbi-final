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
    #create an expander for each prompt
    with st.expander("Prompt 1"):
        st.write("Prompt 1 text")
    with st.expander("Prompt 2"):
        st.write("Prompt 2 text")
    with st.expander("Prompt 3"):
        st.write("Prompt 3 text")
   

with faq:
    st.title("Freqently Asked Questions")
    st.write("Here are some frequently asked questions:")
    