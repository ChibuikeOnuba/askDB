import os
import ast
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from typing import Dict, TypedDict
from langchain import hub
from langchain_openai import ChatOpenAI
from typing_extensions import Annotated

def generate_sql_query(
    query: str, 
    db=None, 
    api_key: str = None
) -> Dict[str, str]:
    """
    Generate SQL query from natural language question
    
    Args:
        query (str): Natural language question
        db (Optional): Database connection object
        api_key (Optional[str]): OpenAI API key
    
    Returns:
        Dict containing generated SQL query
    """
    # Set API key if not provided
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    elif not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OpenAI API key is required")

    # Define output structure
    class QueryOutput(TypedDict):
        query: Annotated[str, ..., "Syntactically valid SQL query."]

    # Pull query prompt template
    query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Prepare prompt context
    prompt_context = {
        "dialect": db.dialect if db else "generic",
        "top_k": 10,
        "table_info": db.get_table_info() if db else "",
        "input": query,
    }

    # Create structured output
    structured_llm = llm.with_structured_output(QueryOutput)
    
    # Generate prompt and invoke LLM
    prompt = query_prompt_template.invoke(prompt_context)
    result = structured_llm.invoke(prompt)

    return {"query": result["query"], "llm":llm}

import ast
def query_sql(db, llm, question, sql: str) -> str:
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    answer = execute_query_tool.invoke(sql)
    parsed_result = ast.literal_eval(answer)

    # Access the first value (48)
    value = parsed_result[0][0]
    
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {question}\n'
        f'SQL Query: {sql}\n'
        f'SQL Result: {value}'
    )
    response = llm.invoke(prompt)
    return response.content