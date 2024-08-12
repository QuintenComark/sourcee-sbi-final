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
    st.write("Example Prompts")
with tipstricks:
    st.write("Tips & Tricks")
with faq:
    st.write("Freqently Asked Questions")