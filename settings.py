import os
import base64
import re
import json
import requests
import streamlit as st
import openai
import time


logo = 'https://nveil.ai/wp-content/uploads/2024/07/sourcee-logo-v2.png'

assistant_id = st.secrets["ASSISTANT_ID"]
open_ai_key = st.secrets["OPENAI_API_KEY"]

openai.api_type = 'openai'

openai.api_key = open_ai_key

st.logo(logo)

sourcee_settings_object = openai.beta.assistants.retrieve(assistant_id)
sourcee_current_temp = sourcee_settings_object.temperature

#write a settings page to adapt the LLM's settings like temperature, max_tokens, etc.
st.title("Settings")
st.write("Adjust the settings of the LLM to your needs:")

st.write("Note: adjusting the temperature will affect the randomness of the responses. A higher temperature will result in more random responses, while a lower temperature will result in more predictable responses. The slider is set on the current temperature of Sourcee.")
#add a slider for the temperature
temperature = st.slider("Temperature", 0.0, 2.0, sourcee_current_temp)



#add a button to save the settings and update the openai llm with the new settings
if st.button("Save Settings"):
    st.write(temperature)
    openai.beta.assistants.update(
        assistant_id,
        temperature=temperature
        )
    st.success("Settings saved successfully!")
    st.write("Please refresh the page to apply the new settings.")
