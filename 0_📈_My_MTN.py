import streamlit as st
st.set_page_config(
    page_title="MyMTN Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)
from config.styles import CSS_STYLES
from utils.data_processing import load_and_preprocess_data, filter_dataframe, create_dataset
from utils.metrics import (calculate_ytd_metrics, 
                            calculate_yearly_target,
                            calculate_downloads_metrics, 
                            calculate_mau_metrics,
                            create_metric_card)
from utils.visualizations import create_agent_performance_chart
import os

def main():
    st.logo(image="images/mtnlong.jpg", size="large")
    
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    
    df = load_and_preprocess_data("data/mymtn.csv")
    
    dataset_path = "mtnghana/mymtn"
    if not os.path.exists(os.path.join("datasets", dataset_path)) or not os.path.isfile(os.path.join("datasets", dataset_path, 'data.parquet')):
        create_dataset(df)
    
    with st.sidebar:
        st.title("MyMTN Dashboard")
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
        is_percentage=True
    )
    
    create_metric_card(
        cols[1],
        "Yearly Target",
        yearly_target
    )
    
    create_metric_card(
        cols[2],
        "Downloads",
        downloads
    )
    
    create_metric_card(
        cols[3],
        "MAU",
        mau
    )
    
    st.markdown('<div class="chart-title">Top 5 Agents Performance</div>', unsafe_allow_html=True)
    fig_top = create_agent_performance_chart(filtered_df, n_agents=5, direction=False)
    st.plotly_chart(fig_top, use_container_width=True, key="top_agents")

    st.markdown('<div class="chart-title">Bottom 5 Agents Performance</div>', unsafe_allow_html=True)
    fig_bottom = create_agent_performance_chart(filtered_df, n_agents=5, direction=True)
    st.plotly_chart(fig_bottom, use_container_width=True, key="bottom_agents")

if __name__ == "__main__":
    main()