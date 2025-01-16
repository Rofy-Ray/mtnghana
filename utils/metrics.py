from typing import Tuple, Union
import pandas as pd
import streamlit as st

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
    delta_value: float,
    delta_percentage: float,
    is_percentage: bool = False
):
    """Create a metric card with title, value, and styled delta"""
    formatted_value = f"{value:.2f}%" if is_percentage else format_number(value)
    
    with col:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{formatted_value}</div>
                {format_delta(delta_value, delta_percentage)}
            </div>
        """, unsafe_allow_html=True)

def calculate_ytd_metrics(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate YTD achievement metrics with validation"""
    if df.empty:
        return 0.0, 0.0, 0.0
        
    current_downloads = df['download'].sum()
    yearly_target = current_downloads * 1.2  # Example: target is 20% higher than current
    achievement_percentage = (current_downloads / yearly_target * 100) if yearly_target > 0 else 0
    
    previous_downloads = current_downloads * 0.95  # Example: assuming 5% lower in previous period
    delta_value = achievement_percentage - (previous_downloads / yearly_target * 100)
    delta_percentage = (delta_value / (previous_downloads / yearly_target * 100)) * 100 if previous_downloads > 0 else 0
    
    return achievement_percentage, delta_value, delta_percentage

def calculate_yearly_target(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate yearly target metrics with validation"""
    if df.empty:
        return 0.0, 0.0, 0.0
        
    current_target = df['download'].sum() * 1.2  # Example: target is 20% higher than current
    previous_target = current_target * 0.95  # Example: previous target
    
    delta_value = current_target - previous_target
    delta_percentage = (delta_value / previous_target * 100) if previous_target > 0 else 0
    
    return current_target, delta_value, delta_percentage

def calculate_downloads_metrics(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate download metrics with validation"""
    if df.empty:
        return 0.0, 0.0, 0.0
        
    current_downloads = df['download'].sum()
    previous_downloads = current_downloads * 0.95  # Example: previous period
    
    delta_value = current_downloads - previous_downloads
    delta_percentage = (delta_value / previous_downloads * 100) if previous_downloads > 0 else 0
    
    return current_downloads, delta_value, delta_percentage

def calculate_mau_metrics(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate MAU metrics with validation"""
    if df.empty:
        return 0.0, 0.0, 0.0
        
    current_mau = df['mau'].sum()
    previous_mau = current_mau * 0.98  # Example: previous period
    
    delta_value = current_mau - previous_mau
    delta_percentage = (delta_value / previous_mau * 100) if previous_mau > 0 else 0
    
    return current_mau, delta_value, delta_percentage