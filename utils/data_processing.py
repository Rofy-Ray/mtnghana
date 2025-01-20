import pandas as pd
from typing import List
import streamlit as st

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
    
    return df

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