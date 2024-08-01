import os
import base64
import re
import json
import requests
import time
import streamlit_authenticator as stauth

import streamlit as st
from streamlit import session_state as ss
import openai
from openai import AssistantEventHandler
from tools import TOOL_MAP
from typing_extensions import override
from dotenv import load_dotenv
import streamlit_authenticator as stauth
from streamlit_pills import pills

import yaml
from yaml.loader import SafeLoader




with open('auth.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

load_dotenv()

logo = 'https://nveil.ai/wp-content/uploads/2024/07/sourcee-logo-v2.png'

st.logo(logo)

st.markdown(
    """
<style>
    .st-emotion-cache-janbn0 {
        flex-direction: row-reverse;
        text-align: right;
    }
    .stChatInput{
        background-color: #FFFFFF !important;
    }

    .stButton button{
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    .st-emotion-cache-1up18o9{
        background-color: transparent !important;
        color: #fff !important;
    }

    .sidebar{
        background-color: #000000 !important;
    
    }

    span[data-testid="stIconMaterial"]{
        color: #fff !important;
        background-color: transparent !important;
    }

    span[data-testid="stIconMaterial"]:hover{
        color: #b24a7a !important;
    }

    textarea[data-testid="stChatInputTextArea"]{
    color: #000 !important;
    caret-color: #000 !important; 
    }

    h1 {
    text-align: center;
    }


</style>
""",
    unsafe_allow_html=True,
)

manatal_api_key = st.secrets["MANATAL_API_KEY"]


def str_to_bool(str_input):
    if not isinstance(str_input, str):
        return False
    return str_input.lower() == "true"


def get_all_candidates():
    url = "https://api.manatal.com/open/v3/candidates/"

    headers = {
        "accept": "application/json",
        "Authorization": f"Token {manatal_api_key}"
    }

    response = requests.get(url, headers=headers)

    return response.text

def get_candidate(email):
    email = email
    url = f"https://api.manatal.com/open/v3/candidates/?email={email}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Token {manatal_api_key}"
    }

    response = requests.get(url, headers=headers)

    return response.text

TOOL_MAP = {
    'get_all_candidates': get_all_candidates,
    'get_candidate': get_candidate,
    # ... other function mappings ...
    # ... other function mappings ...
}


#Secrets for deployment
azure_openai_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]
azure_openai_key = st.secrets["AZURE_OPENAI_KEY"]
openai_api_key = st.secrets["OPENAI_API_KEY"]
authentication_required = str_to_bool(st.secrets["AUTHENTICATION_REQUIRED"])
assistant_id = st.secrets["ASSISTANT_ID"]
#assistant_id = st.sidebar.text_input('Enter Assistant ID', '')
#instructions = st.secrets["RUN_INSTRUCTIONS", ""]
#assistant_title = st.secrets["ASSISTANT_TITLE", "Nveil.ai Demo Bot"]
#enabled_file_upload_message = st.secrets[
#    "ENABLED_FILE_UPLOAD_MESSAGE", "Upload a file"
#]


# Load environment variables
#azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
#azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
#openai_api_key = os.environ.get("OPENAI_API_KEY")
#authentication_required = str_to_bool(os.environ.get("AUTHENTICATION_REQUIRED", False))
#assistant_id = os.environ.get("ASSISTANT_ID")
#assistant_id = st.sidebar.text_input('Enter Assistant ID', '')
#instructions = os.environ.get("RUN_INSTRUCTIONS", "")
#assistant_title = os.environ.get("ASSISTANT_TITLE", "Nveil.ai Demo Bot")
#enabled_file_upload_message = os.environ.get(
#    "ENABLED_FILE_UPLOAD_MESSAGE", "Upload a file"
#)
#sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]



client = None
if azure_openai_endpoint and azure_openai_key:
    client = openai.AzureOpenAI(
        api_key=azure_openai_key,
        api_version="2024-02-15-preview",
        azure_endpoint=azure_openai_endpoint,
    )
else:
    client = openai.OpenAI(api_key=openai_api_key)

my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)


class EventHandler(AssistantEventHandler):
    @override
    def on_event(self, event):
        pass

    @override
    def on_text_created(self, text):
        st.session_state.current_message = ""
        with st.chat_message("Assistant"):
            st.session_state.current_markdown = st.empty()

    @override
    def on_text_delta(self, delta, snapshot):
        if snapshot.value:
            text_value = re.sub(
                r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", "Download Link", snapshot.value
            )
            st.session_state.current_message = text_value
            st.session_state.current_markdown.markdown(
                st.session_state.current_message, True
            )

    @override
    def on_text_done(self, text):
        format_text = format_annotation(text)
        st.session_state.current_markdown.markdown(format_text, True)
        st.session_state.chat_log.append({"name": "assistant", "msg": format_text})

    @override
    def on_tool_call_created(self, tool_call):
        if tool_call.type == "code_interpreter":
            st.session_state.current_tool_input = ""
            with st.chat_message("Assistant"):
                st.session_state.current_tool_input_markdown = st.empty()

    @override
    def on_tool_call_delta(self, delta, snapshot):
        if 'current_tool_input_markdown' not in st.session_state:
            with st.chat_message("Assistant"):
                st.session_state.current_tool_input_markdown = st.empty()

        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                st.session_state.current_tool_input += delta.code_interpreter.input
                input_code = f"### code interpreter\ninput:\n```python\n{st.session_state.current_tool_input}\n```"
                st.session_state.current_tool_input_markdown.markdown(input_code, True)

            if delta.code_interpreter.outputs:
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        pass

    @override
    def on_tool_call_done(self, tool_call):
        st.session_state.tool_calls.append(tool_call)
        if tool_call.type == "code_interpreter":
            if tool_call.id in [x.id for x in st.session_state.tool_calls]:
                return
            input_code = f"### code interpreter\ninput:\n```python\n{tool_call.code_interpreter.input}\n```"
            st.session_state.current_tool_input_markdown.markdown(input_code, True)
            st.session_state.chat_log.append({"name": "assistant", "msg": input_code})
            st.session_state.current_tool_input_markdown = None
            for output in tool_call.code_interpreter.outputs:
                if output.type == "logs":
                    output = f"### code interpreter\noutput:\n```\n{output.logs}\n```"
                    with st.chat_message("Assistant"):
                        st.markdown(output, True)
                        st.session_state.chat_log.append(
                            {"name": "assistant", "msg": output}
                        )
        elif (
            tool_call.type == "function"
            and self.current_run.status == "requires_action"
        ):
            with st.chat_message("Assistant"):
                msg = f"### Function Calling: {tool_call.function.name}"
                st.markdown(msg, True)
                st.session_state.chat_log.append({"name": "assistant", "msg": msg})
            tool_calls = self.current_run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            for submit_tool_call in tool_calls:
                tool_function_name = submit_tool_call.function.name
                tool_function_arguments = json.loads(
                    submit_tool_call.function.arguments
                )
                tool_function_output = TOOL_MAP[tool_function_name](
                    **tool_function_arguments
                )
                tool_outputs.append(
                    {
                        "tool_call_id": submit_tool_call.id,
                        "output": tool_function_output,
                    }
                )

            with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=st.session_state.thread.id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=EventHandler(),
            ) as stream:
                stream.until_done()



def create_thread(content, file):
    messages = [
        {
            "role": "user",
            "content": content,
        }
    ]
    if file is not None:
        messages[0].update({"file_ids": [file.id]})
    thread = client.beta.threads.create()
    return thread


def create_message(thread, content, file):
    attachments = []
    if file is not None:
        attachments.append(
            {"file_id": file.id, "tools": [{"type": "code_interpreter"}]}
        )
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=content, attachments=attachments
    )

def create_message_feedback(thread, feedback_prompt):
    
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=feedback_prompt
    )


def create_file_link(file_name, file_id):
    content = client.files.content(file_id)
    content_type = content.response.headers["content-type"]
    b64 = base64.b64encode(content.text.encode(content.encoding)).decode()
    link_tag = f'<a href="data:{content_type};base64,{b64}" download="{file_name}">Download Link</a>'
    return link_tag


def format_annotation(text):
    citations = []
    text_value = text.value
    for index, annotation in enumerate(text.annotations):
        text_value = text.value.replace(annotation.text, f" [{index}]")
        

        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            print(file_citation)
            
            citations.append(
                f"[{index}] {cited_file.filename}"
            )
        elif file_path := getattr(annotation, "file_path", None):
            link_tag = create_file_link(
                annotation.text.split("/")[-1],
                file_path.file_id,
            )
            text_value = re.sub(r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", link_tag, text_value)
    text_value += "\n\n" + "\n".join(citations)
    return text_value


def run_stream(user_input, file):
    if "thread" not in st.session_state:
        st.session_state.thread = create_thread(user_input, file)
    create_message(st.session_state.thread, user_input, file)
    with client.beta.threads.runs.stream(
        thread_id=st.session_state.thread.id,
        assistant_id=assistant_id,
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()

def run_stream_with_feedback(feedback_prompt):
    
    create_message_feedback(st.session_state.thread, feedback_prompt)
    with client.beta.threads.runs.stream(
        thread_id=st.session_state.thread.id,
        assistant_id=assistant_id,
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
        


def handle_uploaded_file(uploaded_file):
    file = client.files.create(file=uploaded_file, purpose="assistants")
    return file


def render_chat():
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.markdown(chat["msg"], True)
            #if chat["name"] == "assistant":  # Assuming the assistant's name is "Assistant"
            #    feedback = st.feedback("thumbs")
            #    if feedback is not None:
            #        st.markdown(f"You selected: {sentiment_mapping[feedback]}")
            #        st.toast("Thanks for your feedback!")
                    
                    


if "tool_call" not in st.session_state:
    st.session_state.tool_calls = []

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "in_progress" not in st.session_state:
    st.session_state.in_progress = False


def disable_form():
    st.session_state.in_progress = True





    

def main():
   
    st.title("Sourcee AI Platform")
    user_msg = st.chat_input(
        "Ask Sourcee a question...", on_submit=disable_form, disabled=st.session_state.in_progress
    )

    #pills("Label", ["Option 1", "Option 2", "Option 3"], ["🍀", "🎈", "🌈"])

    if st.sidebar.button('Clear chat'):
    # Clear the chat history
        st.session_state.chat_log = []
        # Create a new thread by creating a new assistant session
        # Replace 'Enter Assistant ID' with the actual method to create a new thread
        #st.session_state.thread_id = create_thread("Enter Assistant ID", None).id


    
    if enabled_file_upload_message:
        uploaded_file = st.sidebar.file_uploader(
            enabled_file_upload_message,
            type=[
                "txt",
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "csv",
                "json",
                "geojson",
                "xlsx",
                "xls",
            ],
            disabled=st.session_state.in_progress,
        )
    else:
        uploaded_file = None

    if user_msg:
        render_chat()
        with st.chat_message("user"):
            st.markdown(user_msg, True)
            
        st.session_state.chat_log.append({"name": "user", "msg": user_msg})

        file = None
        if uploaded_file is not None:
            file = handle_uploaded_file(uploaded_file)
        run_stream(user_msg, file)
        
        st.session_state.in_progress = False
        st.session_state.tool_call = None
        st.rerun()

    render_chat()


main()
