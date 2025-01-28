from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
import httpx
from langchain_mistralai import ChatMistralAI

import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

import langchain
langchain.debug = False

db_path = f"sqlite:///data/mymtn.db"

def init_llm():
    llm = ChatMistralAI(
        model="open-codestral-mamba",
        temperature=0,
    )
    return llm

system_role = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
                Question: {question}
                SQL Query: {query}
                SQL Result: {result}
                Answer: 
            """

llm = init_llm()
db = SQLDatabase.from_uri(db_path)

def generate_response(user_message):
    """
    Generate a response to a user's message.

    Args:
    user_message (str): The user's message.

    Returns:
    str: The generated response.
    """
    try:
        execute_query = QuerySQLDataBaseTool(db=db)
        write_query = create_sql_query_chain(llm, db)
        answer_prompt = PromptTemplate.from_template(system_role)
        answer = answer_prompt | llm | StrOutputParser()
        chain = (RunnablePassthrough.assign(query=write_query).assign(result=itemgetter("query") | execute_query) | answer)
        response = chain.invoke({"question": user_message})
        return response
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        error_message = e.response.json().get("message", "Unknown error")
        logging.error(f"HTTP error {status_code}: {error_message}")
        if status_code == 429:
            return "Rate limit exceeded. Please try again later."
        else:
            return f"HTTP error {status_code}: {error_message}"
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return "An error occurred while generating a response."