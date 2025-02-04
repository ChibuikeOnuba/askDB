import streamlit as st
import sqlite3
import os
import pandas as pd
from langchain.utilities import SQLDatabase
from test_util import generate_sql_query, query_sql



def initialize_app():
    # Set page title and configure layout
    st.set_page_config(page_title="Natural Language to SQL Translator", layout="wide")
    
    # Initialize session state variables if they don't exist
    if 'generated_sql' not in st.session_state:
        st.session_state.generated_sql = ""
    if 'query_results' not in st.session_state:
        st.session_state.query_results = None
    

    db_user = "root"
    db_password = "root123"
    db_host = "localhost"
    db_name = "atliq_tshirts"

    try:
        # Attempt to create a database connection
        db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}", sample_rows_in_table_info=3)
        st.success("DATABASE CONNECTED SUCCESSFULLY")
        return db
    except Exception as e:
        # Print failure message and the specific error
        st.error("DATABASE CONNECTION FAILED")
        st.error(f"Error: {str(e)}")
        return None

def translate_to_sql(natural_language, dialect):
    # This is a placeholder function - in a real application, you would integrate
    # with an NL-to-SQL model or API here
    # For demonstration, we'll return a simple example query
    example_queries = {
        "show all users": "SELECT * FROM users;",
        "find oldest customer": "SELECT * FROM customers ORDER BY age DESC LIMIT 1;",
        "total sales by product": "SELECT product_name, SUM(quantity) as total_sales FROM sales GROUP BY product_name;"
    }
    return example_queries.get(natural_language.lower(), "SELECT * FROM table_name;")

def execute_query(sql_query, connection):
    try:
        df = pd.read_sql_query(sql_query, connection)
        return df
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
        return None

def main():
    
    db = initialize_app()
    
    # Sidebar for SQL dialect selection
    with st.sidebar:
        st.title("Settings")
        sql_dialect = st.selectbox(
            "Select SQL Dialect",
            ["SQLite", "PostgreSQL", "MySQL", "SQL Server"],
            key="sql_dialect"
        )
        
        st.markdown("---")
        st.markdown("""
        ### How to use:
        1. Enter your question in natural language
        2. Click 'Translate to SQL' to generate SQL
        3. Edit the SQL if needed
        4. Click 'Run Query' to execute
        """)
 
    
    # Main content area
    st.title("Natural Language to SQL Query Tool")

    
    # Natural language input
    col1, col2 = st.columns(2)
    nl_query = col1.text_area(
        "Enter your question in natural language",
        height=150
    )
    result = result = generate_sql_query(nl_query, db=db)
    sql = result["query"]
    llm = result["llm"]    
    
    # Translate button
    if col1.button("Translate to SQL"):
        if nl_query:
            st.session_state.generated_sql = sql
        elif db is None:
            st.error("Database connection failed")
        else:
            st.error("Please enter natural language query")
    
    # SQL query editor
    sql_query = col2.text_area(
        "Generated SQL (you can edit this)",
        value=st.session_state.generated_sql,
        height=150,
        key="sql_editor"
    )

    st.write("------------")
    
    # Execute query button
    if col2.button("Run Query"):
        if sql_query:
            try:
                response = query_sql(db, question=nl_query, llm=llm,sql=sql_query)
                st.session_state.query_results = response
                st.success("Query executed successfully")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a SQL query to execute")
    
    # Results area
    if st.session_state.query_results is not None:
        st.subheader("Query Results")
        st.write(st.session_state.query_results)

if __name__ == "__main__":
    main()