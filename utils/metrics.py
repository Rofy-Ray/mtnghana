from typing import Tuple, Union
import pandas as pd
import streamlit as st

TARGET_ESTIMATION_MULTIPLIER = 1.2
PREVIOUS_ESTIMATION_MULTIPLIER = 0.95

def format_number(num: float) -> str:
    """Format large numbers with commas and handle NaN"""
    if pd.isna(num):
        return "0"
    return f"{int(num):,}"

def format_delta(value: float, percentage: float) -> str:
    arrow = "↑" if value >= 0 else "↓"
    color_class = "positive" if value >= 0 else "negative"
    formatted_value = format_number(abs(value))
    return f"""<span class="metric-delta-{color_class}">
        {arrow} {formatted_value} ({percentage:+.2f}%)
    </span>"""

def create_metric_card(
    col,
    title: str,
    value: Union[int, float],
    is_percentage: bool = False
) -> None:
    """Create a metric card with title, value, and styled delta"""
    formatted_value = f"{value:.2f}%" if is_percentage else format_number(value)
    
    with col:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{formatted_value}</div>
            </div>
        """, unsafe_allow_html=True)

def calculate_ytd_metrics(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate YTD achievement metrics with validation"""
    if df.empty:
        return 0.0, 0.0, 0.0
        
    current_downloads = df['download'].sum()
    yearly_target = current_downloads * TARGET_ESTIMATION_MULTIPLIER
    achievement_percentage = (current_downloads / yearly_target * 100) if yearly_target > 0 else 0
    
    return achievement_percentage, 0.0, 0.0

def calculate_yearly_target(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate yearly target metrics with validation"""
    if df.empty:
        return 0.0, 0.0, 0.0
        
    current_target = df['download'].sum() * TARGET_ESTIMATION_MULTIPLIER
    
    previous_target = current_target * PREVIOUS_ESTIMATION_MULTIPLIER
    delta_value = current_target - previous_target
    delta_percentage = (delta_value / previous_target * 100) if previous_target > 0 else 0
        
    return current_target, 0.0, 0.0

def calculate_downloads_metrics(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate download metrics with validation"""
    if df.empty:
        return 0.0, 0.0, 0.0
        
    current_downloads = df['download'].sum()
    
    return current_downloads, 0.0, 0.0

def calculate_mau_metrics(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate MAU metrics with validation"""
    if df.empty:
        return 0.0, 0.0, 0.0
        
    current_mau = df['mau'].sum()
    
    return current_mau, 0.0, 0.0