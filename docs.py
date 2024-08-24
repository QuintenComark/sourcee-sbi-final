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
    #create a text list of tips & tricks
    st.write("Here are some tips & tricks to help you get the most out of Sourcee:")
    
    st.write("1. Be clear: Make sure your prompts are clear and concise. This will help the AI generate more accurate responses. Sourcee knows that he is an expert recruitment assistant, but he needs to know what you are looking for.")
    st.write("2. Specify the wanted output to avoid long answers and limit token cost. For example, if you want to know the experience of a candidate, specify that you only want to know the years of experience. Or when asking for a list of candidates, ask Sourcee to only tell you their names, skills, location and current role")
    st.write("3. To avoid loops and unwanted tool calls, specify your place of search. For example: 'please look for a PowerBi engineer in the documents' or 'please tell me the current role of John from Manatal'")
    st.write("4. In order to ensure good performance, be sure to clear your chat or refresh once in a while to avoid cluttered chat threads")
with faq:
    st.title("Freqently Asked Questions")
    st.write("Here are some frequently asked questions:")
    #create a streamlit expander for each question
    with st.expander("How do I get started?"):
        st.write("To get started, simply type your prompt in the chat box and press enter. Sourcee will generate a response based on your prompt.")
    with st.expander("How can I improve the accuracy of the responses?"):
        st.write("To improve the accuracy of the responses, make sure your prompts are clear and concise. You can also specify the wanted output to avoid long answers and limit token cost.")
    with st.expander("How do I clear the chat?"):
        st.write("To clear the chat, simply click the 'Clear Chat' button at the bottom of the chat window.")
    with st.expander("Sourcee seems to be stuck in a loop while calling external tools. What should I do?"):
        st.write("If Sourcee seems to be stuck in a loop while calling external tools, try specifying your place of search. For example: 'please look for a PowerBi engineer in the documents. If that doesn't work, try refreshing the page.")