import streamlit as st
from typing_extensions import TypedDict
from pages.connection import main
import getpass
import os
from langchain import hub
from langchain_openai import ChatOpenAI

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["  OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


# <---------------- Define the SQL query system prompt ---------------->
llm = ChatOpenAI(model="gpt-4o-mini")

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

assert len(query_prompt_template.messages) == 1
from typing_extensions import Annotated


class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(state: State, db):
    """Generate SQL query to fetch information."""
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}




def display_result():
    db = main()
    st.title("Result Page")
    st.write("Value received from form:", db.table_info)

if __name__ == "__main__":
    display_result()

