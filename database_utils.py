import streamlit as st
from typing_extensions import TypedDict
from pages.connection import main

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str


def display_result():
    db = main()
    st.title("Result Page")
    st.write("Value received from form:", db.table_info)

if __name__ == "__main__":
    display_result()

