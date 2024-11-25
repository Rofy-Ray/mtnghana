import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import List, Dict, Tuple, Union
import numpy as np

st.set_page_config(
    page_title="MTN Ghana Dashboard",
    page_icon="images/mtnshort.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

st.logo(image="images/mtnlong.jpg",
        size="large")

st.markdown("""
    <style>
    .stApp {
        background-color: #1a1f2c;
    }
    .metric-container {
        background-color: #2d3748;
        border-radius: 8px;
        padding: 1.5rem;
        border: 1px solid #4a5568;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .metric-title {
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .metric-value {
        color: #ffffff;
        font-weight: bold;
        text-align: center;
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        line-height: 1.2;
        margin: 0.5rem 0;
    }
    .metric-delta-positive {
        color: #4ADE80;
        font-size: 1rem;
        display: block;
        margin-top: 0.5rem;
    }
    .metric-delta-negative {
        color: #FF4D4D;
        font-size: 1rem;
        display: block;
        margin-top: 0.5rem;
    }
    .stSelectbox [data-baseweb="select"] span {
        color: black !important;
    }
    .stMultiSelect [data-baseweb="select"] span {
        color: black !important;
    }
    .sidebar-logo {
        margin-bottom: 2rem;
    }
    .sidebar-logo img {
        max-width: 100%;
        height: auto;
    }
    .chart-title {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_preprocess_data(file_path: str) -> pd.DataFrame:
    """Load and preprocess the MTN data"""
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower()
    
    date_columns = ['date', 'month', 'year']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    
    text_columns = ['salesbusinessunitname', 'servicecentername', 'agentname']
    for col in text_columns:
        df[col] = df[col].str.title()
    
    df['salesbusinessunitname'] = df['salesbusinessunitname'].str.replace(r'\s*\([^)]*\)', '', regex=True)
    
    df[text_columns] = df[text_columns].fillna('N/A')
    df[['download', 'mau']] = df[['download', 'mau']].fillna(0)
    
    return df

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

def format_number(num: float) -> str:
    """Format large numbers with commas and handle NaN"""
    if pd.isna(num):
        return "0"
    return f"{int(num):,}"

def format_delta(value: float, percentage: float) -> str:
    """Format delta with arrow and styling"""
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

def create_agent_performance_chart(df: pd.DataFrame) -> go.Figure:
    """Create a double bar chart for agent performance with validation"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for the selected filters",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(color="white", size=16)
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FFFFFF',
            height=400
        )
        return fig
    
    df_sorted = df.groupby('agentname').agg({
        'download': 'sum',
        'mau': 'sum'
    }).reset_index().sort_values('download', ascending=False).head(10)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Downloads',
        x=df_sorted['agentname'],
        y=df_sorted['download'],
        marker_color='#FFD700' 
    ))
    
    fig.add_trace(go.Bar(
        name='MAU',
        x=df_sorted['agentname'],
        y=df_sorted['mau'],
        marker_color='#FFFFFF' 
    ))
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF',
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF')
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#FFFFFF'),
            tickangle=45
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#FFFFFF')
        )
    )
    
    return fig

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

def main():
    df = load_and_preprocess_data("./my_mtn.csv")
    
    with st.sidebar:
        st.title("MTN Ghana Dashboard")
        st.header("Filters")
        
        business_units = ["All"] + sorted(df['salesbusinessunitname'].unique().tolist())
        selected_units = st.multiselect(
            "Select Business Unit(s)",
            business_units,
            default=["All"]
        )
        
        if "All" in selected_units:
            available_centers = df['servicecentername'].unique()
        else:
            available_centers = df[df['salesbusinessunitname'].isin(selected_units)]['servicecentername'].unique()
        
        selected_centers = st.multiselect(
            "Select Service Center(s)",
            ["All"] + sorted(available_centers.tolist()),
            default=["All"]
        )
    
    filtered_df = filter_dataframe(df, selected_units, selected_centers)
    
    if filtered_df.empty:
        st.warning("No data available for the selected filters. Please adjust your selection.")
    
    ytd_achieved, ytd_delta, ytd_delta_pct = calculate_ytd_metrics(filtered_df)
    yearly_target, target_delta, target_delta_pct = calculate_yearly_target(filtered_df)
    downloads, downloads_delta, downloads_delta_pct = calculate_downloads_metrics(filtered_df)
    mau, mau_delta, mau_delta_pct = calculate_mau_metrics(filtered_df)
    
    cols = st.columns(4)
    
    create_metric_card(
        cols[0],
        "YTD Achieved",
        ytd_achieved,
        ytd_delta,
        ytd_delta_pct,
        is_percentage=True
    )
    
    create_metric_card(
        cols[1],
        "Yearly Target",
        yearly_target,
        target_delta,
        target_delta_pct
    )
    
    create_metric_card(
        cols[2],
        "Downloads",
        downloads,
        downloads_delta,
        downloads_delta_pct
    )
    
    create_metric_card(
        cols[3],
        "MAU",
        mau,
        mau_delta,
        mau_delta_pct
    )
    
    st.markdown('<div class="chart-title">Agent Performance</div>', unsafe_allow_html=True)
    fig = create_agent_performance_chart(filtered_df)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()