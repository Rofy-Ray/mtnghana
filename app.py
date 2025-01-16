import streamlit as st
from config.styles import CSS_STYLES
from utils.data_processing import load_and_preprocess_data, filter_dataframe
from utils.metrics import (calculate_ytd_metrics, 
                            calculate_yearly_target,
                            calculate_downloads_metrics, 
                            calculate_mau_metrics,
                            create_metric_card)
from utils.visualizations import create_agent_performance_chart

def main():
    st.set_page_config(
        page_title="MTN Ghana Dashboard",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items=None
    )
    
    st.logo(image="images/mtnlong.jpg", size="large")
    
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    
    df = load_and_preprocess_data("data/my_mtn.csv")
    
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