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
    # delta_value: float,
    # delta_percentage: float,
    # weekly_delta: float = None,
    # weekly_delta_pct: float = None,
    is_percentage: bool = False
) -> None:
    """Create a metric card with title, value, and styled delta"""
    formatted_value = f"{value:.2f}%" if is_percentage else format_number(value)
    
    # delta_str = format_delta(delta_value, delta_percentage)
    
    # if weekly_delta is not None and weekly_delta_pct is not None:
    #     weekly_delta_str = format_delta(weekly_delta, weekly_delta_pct)
    # else:
    #     weekly_delta_str = ""
    
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
    
    # previous_downloads = current_downloads * PREVIOUS_ESTIMATION_MULTIPLIER
    # delta_value = achievement_percentage - (previous_downloads / yearly_target * 100)
    # delta_percentage = (delta_value / (previous_downloads / yearly_target * 100)) * 100 if previous_downloads > 0 else 0
    
    # return achievement_percentage, delta_value, delta_percentage
    
    return achievement_percentage, 0.0, 0.0

def calculate_yearly_target(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate yearly target metrics with validation"""
    if df.empty:
        return 0.0, 0.0, 0.0
        
    current_target = df['download'].sum() * TARGET_ESTIMATION_MULTIPLIER
    
    previous_target = current_target * PREVIOUS_ESTIMATION_MULTIPLIER
    delta_value = current_target - previous_target
    delta_percentage = (delta_value / previous_target * 100) if previous_target > 0 else 0
    
    # return current_target, delta_value, delta_percentage
    
    return current_target, 0.0, 0.0

def calculate_downloads_metrics(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate download metrics with validation"""
    if df.empty:
        return 0.0, 0.0, 0.0
        
    current_downloads = df['download'].sum()
    
    # previous_downloads = current_downloads * PREVIOUS_ESTIMATION_MULTIPLIER
    # delta_value = current_downloads - previous_downloads
    # delta_percentage = (delta_value / previous_downloads * 100) if previous_downloads > 0 else 0
    
    # return current_downloads, delta_value, delta_percentage
    
    return current_downloads, 0.0, 0.0

def calculate_mau_metrics(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate MAU metrics with validation"""
    if df.empty:
        return 0.0, 0.0, 0.0
        
    current_mau = df['mau'].sum()
    
    # previous_mau = current_mau * PREVIOUS_ESTIMATION_MULTIPLIER
    # delta_value = current_mau - previous_mau
    # delta_percentage = (delta_value / previous_mau * 100) if previous_mau > 0 else 0
    
    # return current_mau, delta_value, delta_percentage
    
    return current_mau, 0.0, 0.0

# def calculate_weekly_metrics(df: pd.DataFrame) -> Tuple[Tuple[float, float], Tuple[float, float]]:
#     latest_date = df.index.max()
#     previous_week_start = latest_date - pd.Timedelta(days=7)
#     previous_week_end = previous_week_start + pd.Timedelta(days=6)
    
#     if not df.empty:
#         current_downloads = df.loc[[latest_date], 'download'].sum()
#         previous_downloads = df.loc[(df.index >= previous_week_start) & (df.index <= previous_week_end), 'download'].sum()
#         current_mau = df.loc[latest_date, 'mau'].sum()
#         previous_mau = df.loc[(df.index >= previous_week_start) & (df.index <= previous_week_end), 'mau'].sum()
#     else:
#         current_downloads = 0
#         previous_downloads = 0
#         current_mau = 0
#         previous_mau = 0
    
#     downloads_delta = current_downloads - previous_downloads
#     downloads_delta_pct = (downloads_delta / previous_downloads) * 100 if previous_downloads > 0 else 0
    
#     mau_delta = current_mau - previous_mau
#     mau_delta_pct = (mau_delta / previous_mau) * 100 if previous_mau > 0 else 0
    
#     return (downloads_delta, downloads_delta_pct), (mau_delta, mau_delta_pct)