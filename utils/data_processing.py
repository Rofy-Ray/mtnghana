import pandas as pd
from typing import List
import streamlit as st
from sqlalchemy import create_engine, inspect
import logging

logging.basicConfig(level=logging.INFO)

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


db_path = f"sqlite:///data/mymtn.db"
engine = create_engine(db_path)
    
def validate_sql_db() -> bool:
    """Validate if 'mymtn' table exists in SQL database"""
    try:
        inspector = inspect(engine)
        exists = "mymtn" in inspector.get_table_names()
        if not exists:
            logging.error("SQL database missing 'mymtn' table")
        return exists
    except Exception as e:
        logging.error(f"Database validation failed: {str(e)}")
        return False

@st.cache_resource
def create_sql_db_from_df(df: pd.DataFrame) -> bool:
    """Create SQL database from dataframe if it doesn't exist"""
    if validate_sql_db():
        logging.info("Database already exists, skipping creation")
        return True
    df.to_sql(name="mymtn", con=engine, if_exists="replace", index=False)
    logging.info(f"SQL database created at {db_path}")
    return validate_sql_db()

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