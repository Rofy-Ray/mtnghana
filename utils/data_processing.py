import pandas as pd
from typing import List
import streamlit as st
import pandasai as pai
import tempfile
import os
import logging

logging.basicConfig(level=logging.INFO)

pai.api_key.set(os.getenv("PANDASAI_API_KEY"))

@st.cache_data
def load_and_preprocess_data(file_path: str) -> pd.DataFrame:
    """Load and preprocess the MTN data"""
    df = pd.read_csv(file_path)
    
    df.columns = df.columns.str.lower()
    
    df['date_key'] = pd.to_datetime(df['date_key'], format='%Y%m%d')
    
    df['year'] = df['date_key'].dt.year
    df['month'] = df['date_key'].dt.month
    df['day'] = df['date_key'].dt.day
    
    df.set_index('date_key', inplace=True)
    
    text_columns = ['salesbusinessunitname', 'servicecentername', 'agentname']
    for col in text_columns:
        df[col] = df[col].str.title()
    
    df['salesbusinessunitname'] = df['salesbusinessunitname'].str.replace(r'\s*\([^)]*\)', '', regex=True)
    
    df[text_columns] = df[text_columns].fillna('N/A')
    df[['download', 'mau']] = df[['download', 'mau']].fillna(0)
    
    df = df[df['salesbusinessunitname'] == 'Eastern Volta']
    
    return df

def create_dataset(df):
    """
    Create a dataset for the agent.
    """
    temp_path = None
    dataset_path = "mtnghana/mymtn"
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_path = temp_file.name
            df.to_csv(temp_path, index=False)
        pdf = pai.read_csv(temp_path)
        if os.path.exists(os.path.join("datasets", dataset_path)) and os.path.isfile(os.path.join("datasets", dataset_path, 'data.parquet')):
            logging.info(f"Dataset exists at {dataset_path}, skipping creation.")
        else:
            mymtn = pai.create(
                path=dataset_path,
                df=pdf,
                description="""
                This dataset tracks digital service performance metrics (e.g., downloads, monthly active users) across sales business units, service centers, and individual agents. It includes granular details such as geographic regions, service locations, agent names, and daily records of activity. The data enables analysis of operational efficiency, agent productivity, and user engagement trends over time.
                """,
                columns=[
                    {
                        "name": "date_key",
                        "type": "integer",
                        "description": "The date of the record in YYYYMMDD format"
                    },
                    {
                        "name": "salesbusinessunitname",
                        "type": "string",
                        "description": "The name of the sales business unit"
                    },
                    {
                        "name": "servicecentername",
                        "type": "string",
                        "description": "The name of the service center"
                    },
                    {
                        "name": "agentname",
                        "type": "string",
                        "description": "The name of the agent"
                    },
                    {
                        "name": "download",
                        "type": "integer",
                        "description": "The number of downloads"
                    },
                    {
                        "name": "mau",
                        "type": "integer",
                        "description": "The number of monthly active users"
                    },{
                        "name": "year",
                        "type": "integer",
                        "description": "The year from the date of the record in YYYY format"
                    },
                    {
                        "name": "month",
                        "type": "integer",
                        "description": "The month from the date of the record in MM format"
                    },
                    {
                        "name": "day",
                        "type": "integer",
                        "description": "The day from the date of the record in DD format"
                    }
                ]
            )
            mymtn.push()
            logging.info(f"Dataset created at {dataset_path} and pushed to PandasAI.")
    except Exception as e:
        logging.error(f"Dataset creation failed: {str(e)}")
        raise
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            logging.info(f"Cleaned up temporary file: {temp_path}")

def filter_dataframe(
    df: pd.DataFrame,
    selected_units: List[str],
    selected_centers: List[str]
) -> pd.DataFrame:
    """Filter dataframe based on selected units and centers with validation"""
    if not selected_units or not selected_centers:
        return pd.DataFrame() 
        
    filtered_df = df.copy()
    if "All" not in selected_units:
        filtered_df = filtered_df[filtered_df['salesbusinessunitname'].isin(selected_units)]
    if "All" not in selected_centers:
        filtered_df = filtered_df[filtered_df['servicecentername'].isin(selected_centers)]
    
    return filtered_df