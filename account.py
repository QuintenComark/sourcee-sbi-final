import streamlit as st
import streamlit_authenticator as stauth
from sshtunnel import SSHTunnelForwarder

import mysql.connector
import bcrypt

config = {
  'host':'sourcee-users-db.mysql.database.azure.com',
  'user':'qceuppens',
  'password':'Nveil!Sourcee2024',
  'database':'sbi-users'
}

# Connect to the MySQL database
def get_db_connection():
    #return mysql.connector.connect(
    #    host='ID438563_sourceesbi.db.webhosting.be',
    #    user='ID438563_sourceesbi',
    #    password='Nveil!Sourcee2024',
    #    database='ID438563_sourceesbi'
    #)


    
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return conn
    


def fetch_credentials():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, firstname, password, email FROM sbiusers")
    rows = cursor.fetchall()
    
    credentials = {'usernames': {}}
    for row in rows:
        username, firstname, password, email = row
        credentials['usernames'][username] = {
            'name': firstname,
            'password': password,
            'email': email
        }
    
    cursor.close()
    conn.close()
    return credentials


def st_authenticator():
    credentials = fetch_credentials()
    return stauth.Authenticate(
        credentials,
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

    
    
    
user_firstname = st.session_state.name


# Check the authentication status and navigate accordingly
if st.session_state.authentication_status:
    #set logout button in sidebar
    
    authenticator.logout('**Logout**', 'sidebar', key='unique_key')
    
    
    chat_page = st.Page("app.py", title="Chat", icon=":material/add_circle:")
    upload_page = st.Page("upload.py", title="Upload", icon=":material/folder:")
    docs_page = st.Page("docs.py", title="Docs", icon=":material/help:")
    settings_page = st.Page("settings.py", title="Settings", icon=":material/settings:")
    profile_page = st.Page("profile.py", title=user_firstname, icon=":material/person:")
    
    pg = st.navigation([chat_page, upload_page, docs_page, settings_page, profile_page])
    pg.run()
elif st.session_state.authentication_status is False:
    st.error('Username/password is incorrect')
elif st.session_state.authentication_status is None:
    st.warning('Please enter your username and password')
