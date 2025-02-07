import streamlit as st
import pandasai as pai
import os
import logging
from utils.data_processing import load_and_preprocess_data
from pandasai_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

llm = OpenAI(api_token=os.getenv("OPENAI_API_KEY"))

pai.config.set({"llm": llm})

@st.cache_resource 
def load_dataset(path):
    """
    Load the dataset from pandasai organization.
    """
    try:
        df = pai.load(path)
        return df
    except Exception as e:
        logging.error(f"Error loading dataset: {e}")
        
sdf = load_dataset("mtnghana/mymtn")
    
def generate_response(user_message):
    """
    Generate a response to a user's question.

    Args:
    user_message (str): The user's question.

    Returns:
    str: The generated response.
    """
    try:
        response = sdf.chat(user_message)
        return response
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return "An error occurred while generating a response."
