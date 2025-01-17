import streamlit as st
from langchain.utilities import SQLDatabase
import os

def initialize_connection_state():
    """Initialize session state variables."""
    if 'db_connected' not in st.session_state:
        st.session_state.db_connected = False
    if 'db_chain' not in st.session_state:
        st.session_state.db_chain = None
    if 'db_engine' not in st.session_state:
        st.session_state.db_engine = None

def main():
    st.title("Database Connection")
    
    initialize_connection_state()
    
    with st.form("db_credentials"):
        st.subheader("Database Credentials")
        
        dialect = st.selectbox(
            "Select Database Type",
            ["PostgreSQL", "MySQL", "SQL Server"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            host = st.text_input("Host", "localhost")
            port = st.text_input("Port", "5432")
            database = st.text_input("Database Name")
        
        with col2:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            openai_api_key = st.text_input("OpenAI API Key", type="password")
        
        connect_button = st.form_submit_button("Connect to Database")
        
        if connect_button:
            if not openai_api_key:
                st.error("Please provide your OpenAI API key")
                return
            
            os.environ["OPENAI_API_KEY"] = openai_api_key
            

            db_user = username
            db_password = password
            db_host = host
            db_name = database

            try:
                # Attempt to create a database connection
                db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}", sample_rows_in_table_info=3)
                st.markdown("---")
                st.success(f"{db_name.upper()} DATABASE CONNECTED SUCCESSFULLY")
                st.write("Proceed to the Home page to start querying the database.")
            except Exception as e:
                # Print failure message and the specific error
                st.markdown("---")
                st.success("DATABASE CONNECTION FAILED")
                st.write(f"Error: {str(e)}")
                exit(1)
                
    cols = st.columns(4)           
    cols[3].button(type="primary", label="Connect another database")   
             
    return db
        
    

if __name__ == "__main__":
    main()
