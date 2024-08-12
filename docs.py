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
    with st.expander("Tell me about..."):
        st.write("Tell me about 'name of teammember'. For example: what are their strengths and weaknesses, what is their experience, what are their skills, etc.")
    with st.expander("Help me find..."):
        st.write("Help me find a 'name of role'. The candidate should have experience in 'skill', 'skill', and 'skill'. A minimum of 'years' years of experience is required. Only tell me his name, contact info and a brief summary of his experience.")
    with st.expander("Help me write..."):
        st.write("Help me write an engaging text to introduce 'name of teammember'. The text should be professional and engaging, and should highlight their strengths and experience.")
with tipstricks:
    st.title("Tips & Tricks")
with faq:
    st.title("Freqently Asked Questions")
    st.write("Here are some frequently asked questions:")
    