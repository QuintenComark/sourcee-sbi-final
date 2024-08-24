import streamlit as st
import openai
import bcrypt
import mysql.connector
from mysql.connector import errorcode

st.title("Profile settings")

logo = 'https://nveil.ai/wp-content/uploads/2024/07/sourcee-logo-v2.png'
st.logo(logo)

config = {
  'host':'sourcee-users-db.mysql.database.azure.com',
  'user':'qceuppens',
  'password':'Nveil!Sourcee2024',
  'database':'sbi-users'
}


# Connect to the MySQL database
def get_db_connection():
   
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


profile, password = st.tabs(["My profile", "Password"])



def verify_password(current_password):

    current_user = st.session_state.username
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT password FROM sbiusers WHERE username = %s"
    cursor.execute(query, (current_user,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result is None:
        return False
    
    hashed_password = result[0]
    return bcrypt.checkpw(current_password.encode('utf-8'), hashed_password.encode('utf-8'))
    pass

def update_password_in_database(hashed_password):
    if new_password != confirm_password:
        st.error("New password and confirm password do not match.")     
        
    else:
        
        current_user = st.session_state.username
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "UPDATE sbiusers SET password = %s WHERE username = %s"
        cursor.execute(query, (hashed_password, current_user))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Password updated successfully.")
        
        pass




with profile:
    
    #firstname = st.session_state.firstname
    #lastname = st.session_state.lastname
    email = st.session_state.email
    username = st.session_state.username

    def fetch_credentials():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, firstname, lastname, email FROM sbiusers")
        rows = cursor.fetchall()
        
        credentials = {'usernames': {}}

        for row in rows:
            username, firstname, lastname, email = row
            credentials['usernames'][username] = {
                'firstname': firstname,
                'lastname': lastname,
                'email': email
            }
        
        cursor.close()
        conn.close()
        return credentials
    

    credentials = fetch_credentials()
    firstname = credentials['usernames'][username]['firstname']
    lastname = credentials['usernames'][username]['lastname']
    email = credentials['usernames'][username]['email']


    with st.form('profile_settings'):
        st.write("Check and update your personal details")
        form_firstname = st.text_input("Firstname", firstname)
        form_lastname = st.text_input("Lastname", lastname)
        form_email = st.text_input("Email", email)
        if st.form_submit_button("Submit"):
            # Update the user's data in the database
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "UPDATE sbiusers SET firstname = %s, lastname = %s, email = %s WHERE username = %s"
            cursor.execute(query, (form_firstname, form_lastname, form_email, username))
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Profile updated successfully.")
            pass

with password:
    
    # Get user input
    with st.form("change"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.form_submit_button("Submit"):
            # Check if new password matches confirm password
            if not verify_password(current_password):
                st.error("Password does not match the database!")
            else:
                # Hash the new password
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                # Update the password in the databasee
                update_password_in_database(hashed_password)

                
   


