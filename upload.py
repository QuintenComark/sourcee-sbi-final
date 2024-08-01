import os
import base64
import re
import json
import requests
import streamlit as st
import openai
import time

import docx2txt
import pymupdf
import pymupdf4llm

file_id_vd = 'file_id'

vector_store_id = st.secrets["OPENAI_VECTOR_STORE_ID"]
assistant_id = st.secrets["HELPER_ASSISTANT_ID"]
make_api_key = st.secrets["MAKE_API_KEY"]
open_ai_key = st.secrets["OPENAI_API_KEY"]

#vector_store_id = os.environ.get("OPENAI_VECTOR_STORE_ID")
#assistant_id = os.environ.get("HELPER_ASSISTANT_ID")

logo = 'https://nveil.ai/wp-content/uploads/2024/07/sourcee-logo-v2.png'

st.logo(logo)

def docx_to_txt(docx_file_to_parse):
    
    text = docx2txt.process(docx_file_to_parse)

    start_make_scenario(text)

    print(text)

def pdf_to_txt(pdf_file_to_parse):
    with st.spinner('Extracting PDF...'):
        pdf_doc = pymupdf.open(stream=pdf_file_to_parse.read(), filetype="pdf")
        text_filename = pdf_file_to_parse.name.replace(".pdf", "") + ".txt" # create a text output file
        text_output = open(text_filename, "wb") # create a text output


        md_text = pymupdf4llm.to_markdown(pdf_doc)

        #with pymupdf.open(pdf_doc) as doc:  # open document
        #    text = chr(12).join([page.get_text() for page in doc])
        #for page in pdf_doc: # iterate the document pages
        #    text = page.get_text() # get plain text (is in UTF-8)
            #text_output.write(text) # write text of page
            #text_output.write(bytes((12,))) # write page delimiter (form feed 0x0C)
        
        #text.close()

        start_make_scenario(md_text)

    #st.write(md_text)
    #print(md_text)



def upload_to_openai(vector_store_file):
    # Set up OpenAI API
    openai.api_key = open_ai_key

    # Upload file to OpenAI
    response = openai.files.create(file=vector_store_file, purpose='assistants')
    global file_id_vd
    file_id_vd = response.id

    thread = openai.beta.threads.create()

    print(file_id_vd)
       

    message = openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"Always answer with the following: Resume of *insert name of candidate* has been succesfully parsed and stored in the database.",
        attachments=[
            {
                "file_id": file_id_vd,
                "tools": [{"type":"file_search"}]  # Add the required tools or leave it empty if no tools are needed
            }
        ]
    )
    
    run = openai.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions="You are a helpful AI assistant."
      
    )

    if run.status == 'completed':
        messages = openai.beta.threads.messages.list(
            thread_id=thread.id
        )
        for message in messages.data:
            if message.role == 'assistant':
                answer = message.content[0].text.value
     
    else:
        print(run.status)

    st.markdown(answer, unsafe_allow_html=False, help=None)

    print(file_id_vd)
    #REMOVE THIS CODE AFTER TESTING
    #openai.files.delete(file_id_vd)
    print(run)

    

    upload_to_vector_database(vector_store_file, file_id_vd)
    
    return response.id

def upload_to_vector_database(vector_store_file, file_id_vd):
   
    vector_store_file = openai.beta.vector_stores.files.create(
        vector_store_id=vector_store_id,
        file_id=file_id_vd
    )


    print(vector_store_file)

def start_make_scenario(text):
    url = "https://eu2.make.com/api/v2/scenarios/1416486/run"
    #url = "https://eu2.make.com/api/v2/scenarios/1562841/run"

    payload = json.dumps({
    "data": {
        "Text": text
        }
    })
    headers = {
        'Authorization': f'Token {make_api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    return "somthing" 

def upload_main():
    st.title('File Upload to Parse')

    vector_store_file = st.file_uploader('Upload a file to the vector store')
    if vector_store_file is not None:
        if st.button('Upload'):
            # Upload file to OpenAI
            
            with st.spinner('Checking file type...'):
                if vector_store_file.name.endswith('.docx'):
                    openai_file_id = upload_to_openai(vector_store_file)
                    docx_file_to_parse = docx_to_txt(vector_store_file)
                    
                elif vector_store_file.name.endswith('.pdf'):
                    
                    pdf_file_to_parse = pdf_to_txt(vector_store_file)
                    openai_file_id = upload_to_openai(vector_store_file)
                else:
                    st.write('File type not supported. Please upload a .docx or .pdf file.')
                

            
                st.write(f'You will receive an email when your file is ready.')



upload_main()
