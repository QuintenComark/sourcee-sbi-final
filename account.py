import streamlit as st
import streamlit_authenticator as stauth



def st_authenticator():
    return stauth.Authenticate(
        st.secrets['credentials'].to_dict(),
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days'],
        st.secrets['preauthorized']
        
    )



# Initialize the session state variables if they do not exist
if "authenticator" not in st.session_state:
    st.session_state.authenticator = st_authenticator()
    st.session_state.name = None
    st.session_state.authentication_status = None
    st.session_state.username = None
    st.session_state.email = None
    
   

authenticator = st.session_state.authenticator


# Only run the login process if the user is not already authenticated
if st.session_state.authentication_status is None:
   
    
    name, authentication_status, username = authenticator.login("main")
    st.session_state.name = name
    st.session_state.authentication_status = authentication_status
    st.session_state.username = username

    
    
    
  
    


# Check the authentication status and navigate accordingly
if st.session_state.authentication_status:
    #set logout button in sidebar
    
    authenticator.logout('**Logout**', 'sidebar', key='unique_key')
    
    chat_page = st.Page("app.py", title="Chat", icon=":material/add_circle:")
    upload_page = st.Page("upload.py", title="Upload", icon=":material/delete:")
    docs_page = st.Page("docs.py", title="Docs", icon=":material/help:")
    
    pg = st.navigation([chat_page, upload_page, docs_page])
    pg.run()
elif st.session_state.authentication_status is False:
    st.error('Username/password is incorrect')
elif st.session_state.authentication_status is None:
    st.warning('Please enter your username and password')
