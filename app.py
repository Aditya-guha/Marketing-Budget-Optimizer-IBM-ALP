import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import io
from utils.data_processor import process_data, validate_data
from utils.optimizer import optimize_budget
from utils.visualizer import (
    plot_roi_by_platform,
    plot_cpa_vs_conversion,
    plot_time_series,
    plot_budget_allocation,
    plot_expected_returns
)

# Set page configuration
st.set_page_config(
    page_title="ALP IBM Budget Optimizer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for better UI
st.markdown("""
<style>
    .main {
        padding: 1rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4e8df5;
        color: white;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'optimization_result' not in st.session_state:
    st.session_state.optimization_result = None
if 'total_budget' not in st.session_state:
    st.session_state.total_budget = 10000

# Title and introduction
st.title("💰 ALP IBM Budget Optimizer by Aditya MBA BA 24023184")
st.markdown("""
This application helps digital marketing agencies optimize their ad budget allocation across multiple platforms.
Upload your campaign data, analyze performance trends, and get AI-powered budget allocation recommendations.
""")

# Sidebar for data upload and configuration
with st.sidebar:
    st.header("📊 Data Input")
    
    uploaded_file = st.file_uploader("Upload Campaign Data (CSV)", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Cache data loading
            @st.cache_data
            def load_data(file):
                return pd.read_csv(file)
            
            data = load_data(uploaded_file)
            
            # Validate data
            validation_result = validate_data(data)
            
            if validation_result["valid"]:
                st.session_state.data = data
                st.success(f"✅ Data loaded successfully! ({len(data)} rows)")
                
                # Process data for optimization
                st.session_state.processed_data = process_data(data)
            else:
                st.error(f"❌ {validation_result['message']}")
                st.info("Required columns: Channel_Used, ROI, Conversion_Rate, Acquisition_Cost")
                st.session_state.data = None
                st.session_state.processed_data = None
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.session_state.data = None
            st.session_state.processed_data = None
    
    st.divider()
    
    # Budget input
    st.header("💵 Budget Configuration")
    total_budget = st.number_input(
        "Total Budget ($)",
        min_value=1000,
        max_value=10000000,
        value=st.session_state.total_budget,
        step=1000,
        help="Enter the total budget you want to allocate across platforms"
    )
    st.session_state.total_budget = total_budget
    
    # Date range filter (if data is loaded)
    if st.session_state.data is not None and 'Date' in st.session_state.data.columns:
        st.header("📅 Date Range")
        
        # Convert date column to datetime
        st.session_state.data['Date'] = pd.to_datetime(st.session_state.data['Date'])
        
        min_date = st.session_state.data['Date'].min().date()
        max_date = st.session_state.data['Date'].max().date()
        
        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_data = st.session_state.data[
                (st.session_state.data['Date'].dt.date >= start_date) & 
                (st.session_state.data['Date'].dt.date <= end_date)
            ]
            st.session_state.processed_data = process_data(filtered_data)
            st.info(f"Filtered to {len(filtered_data)} rows from {start_date} to {end_date}")

# Main content
if st.session_state.data is None:
    # Show sample data option when no data is uploaded
    st.info("👈 Please upload your campaign data CSV file from the sidebar to get started.")
    
    if st.button("🔍 Use Sample Data for Demo"):
        # Generate sample data
        @st.cache_data
        def generate_sample_data():
            np.random.seed(42)
            platforms = ['Google Ads', 'Facebook Ads', 'LinkedIn Ads', 'Twitter Ads', 'Instagram Ads']
            companies = ['TechCorp', 'FashionBrand', 'FoodDelivery', 'FinanceApp', 'TravelAgency']
            audiences = ['Young Adults', 'Professionals', 'Parents', 'Seniors', 'Students']
            campaign_types = ['Awareness', 'Conversion', 'Retargeting', 'Lead Generation']
            locations = ['US', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'Japan']
            languages = ['English', 'Spanish', 'French', 'German', 'Japanese']
            segments = ['High Value', 'Mid Value', 'Low Value', 'New Customer', 'Returning']
            
            n_samples = 1000
            
            # Generate dates for the last 6 months
            end_date = datetime.now()
            start_date = end_date - timedelta(days=180)
            dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days)]
            
            data = {
                'Campaign_ID': [f'CAMP{i:04d}' for i in range(1, n_samples+1)],
                'Company': np.random.choice(companies, n_samples),
                'Campaign_Type': np.random.choice(campaign_types, n_samples),
                'Target_Audience': np.random.choice(audiences, n_samples),
                'Duration': np.random.randint(7, 90, n_samples),
                'Channel_Used': np.random.choice(platforms, n_samples),
                'Conversion_Rate': np.random.uniform(0.01, 0.15, n_samples),
                'Acquisition_Cost': np.random.uniform(5, 100, n_samples),
                'ROI': np.random.uniform(0.5, 5, n_samples),
                'Location': np.random.choice(locations, n_samples),
                'Language': np.random.choice(languages, n_samples),
                'Clicks': np.random.randint(100, 10000, n_samples),
                'Impressions': np.random.randint(1000, 100000, n_samples),
                'Engagement_Score': np.random.uniform(0.1, 1.0, n_samples),
                'Customer_Segment': np.random.choice(segments, n_samples),
                'Date': np.random.choice(dates, n_samples)
            }
            
            # Adjust ROI based on platform (make some platforms perform better)
            platform_multipliers = {
                'Google Ads': 1.2,
                'Facebook Ads': 1.1,
                'LinkedIn Ads': 0.9,
                'Twitter Ads': 0.8,
                'Instagram Ads': 1.0
            }
            
            for i in range(n_samples):
                platform = data['Channel_Used'][i]
                data['ROI'][i] *= platform_multipliers[platform]
            
            df = pd.DataFrame(data)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        
        sample_data = generate_sample_data()
        st.session_state.data = sample_data
        st.session_state.processed_data = process_data(sample_data)
        st.success("✅ Sample data loaded successfully!")
        st.rerun()
else:
    # Create tabs for different sections
    tabs = st.tabs(["📊 Data Overview", "📈 Exploratory Analysis", "🤖 Budget Optimizer", "📱 Dashboard"])
    
    # Tab 1: Data Overview
    with tabs[0]:
        st.header("Campaign Data Overview")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Campaigns", len(st.session_state.data))
        
        with col2:
            if 'Channel_Used' in st.session_state.data.columns:
                st.metric("Platforms", st.session_state.data['Channel_Used'].nunique())
        
        st.subheader("Data Sample")
        st.dataframe(st.session_state.data.head(10), use_container_width=True)
        
        st.subheader("Data Summary")
        
        # Show summary statistics for numerical columns
        numeric_cols = st.session_state.data.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) > 0:
            st.dataframe(st.session_state.data[numeric_cols].describe(), use_container_width=True)
        
        # Show platform distribution
        if 'Channel_Used' in st.session_state.data.columns:
            st.subheader("Platform Distribution")
            platform_counts = st.session_state.data['Channel_Used'].value_counts().reset_index()
            platform_counts.columns = ['Platform', 'Count']
            
            fig = px.pie(
                platform_counts, 
                values='Count', 
                names='Platform',
                title='Campaign Distribution by Platform',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Exploratory Analysis
    with tabs[1]:
        st.header("Exploratory Data Analysis")
        
        if st.session_state.processed_data is not None:
            # ROI by Platform
            st.subheader("ROI by Platform")
            roi_fig = plot_roi_by_platform(st.session_state.processed_data)
            st.plotly_chart(roi_fig, use_container_width=True)
            
            # CPA vs Conversion Rate
            st.subheader("Cost Per Acquisition vs Conversion Rate")
            cpa_conv_fig = plot_cpa_vs_conversion(st.session_state.processed_data)
            st.plotly_chart(cpa_conv_fig, use_container_width=True)
            
            # Time Series Analysis (if Date column exists)
            if 'Date' in st.session_state.data.columns:
                st.subheader("Performance Over Time")
                
                metric_options = ['ROI', 'Conversion_Rate', 'Clicks', 'Impressions', 'Acquisition_Cost']
                available_metrics = [m for m in metric_options if m in st.session_state.data.columns]
                
                if available_metrics:
                    selected_metric = st.selectbox("Select Metric", available_metrics)
                    time_fig = plot_time_series(st.session_state.data, selected_metric)
                    st.plotly_chart(time_fig, use_container_width=True)
    
    # Tab 3: Budget Optimizer
    with tabs[2]:
        st.header("AI Budget Allocation Optimizer")
        
        if st.session_state.processed_data is not None:
            st.info(f"Total Budget: ${st.session_state.total_budget:,.2f}")
            
            if st.button("🚀 Optimize Budget Allocation"):
                with st.spinner("Optimizing budget allocation..."):
                    # Run optimization
                    optimization_result = optimize_budget(
                        st.session_state.processed_data,
                        st.session_state.total_budget
                    )
                    st.session_state.optimization_result = optimization_result
            
            # Display optimization results
            if st.session_state.optimization_result is not None:
                st.success("✅ Budget optimization completed!")
                
                result_df = st.session_state.optimization_result
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Budget Allocation")
                    budget_fig = plot_budget_allocation(result_df)
                    st.plotly_chart(budget_fig, use_container_width=True, key="budget_tab3")
                
                with col2:
                    st.subheader("Expected Returns")
                    returns_fig = plot_expected_returns(result_df)
                    st.plotly_chart(returns_fig, use_container_width=True, key="returns_tab3")
                
                st.subheader("Detailed Allocation")
                st.dataframe(result_df, use_container_width=True)
                
                # Download button for results
                csv = result_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Budget Allocation as CSV",
                    data=csv,
                    file_name="budget_allocation.csv",
                    mime="text/csv"
                )
                
                # AI Recommendations button
                st.divider()
                if st.button("🤖 Show AI-Based Recommendations", key="ai_recommendations"):
                    st.subheader("AI-Based Investment Recommendations")
                    
                    # Create recommendations based on optimization results
                    st.markdown("### Why This Allocation Works")
                    st.write(
                        "This AI-optimized budget allocation is designed to maximize your return on investment "
                        "based on historical performance data across different platforms. The allocation "
                        "prioritizes channels with higher ROI while ensuring sufficient budget for all platforms."
                    )
                    
                    # Top performing platforms
                    top_platforms = result_df.sort_values('ROI', ascending=False).head(2)['Platform'].tolist()
                    st.markdown("### Top Performing Platforms")
                    st.write(
                        f"Based on your data, **{' and '.join(top_platforms)}** show the highest ROI. "
                        f"The model has allocated more budget to these platforms to maximize returns."
                    )
                    
                    # Expected outcomes
                    total_return = result_df['Expected_Return'].sum()
                    roi_percentage = ((total_return / st.session_state.total_budget) - 1) * 100
                    st.markdown("### Expected Outcomes")
                    st.write(
                        f"With this allocation, you can expect a total return of **${total_return:,.2f}** "
                        f"on your ${st.session_state.total_budget:,.2f} investment, representing an overall "
                        f"ROI of **{roi_percentage:.2f}%**."
                    )
                    
                    # Strategic recommendations
                    st.markdown("### Strategic Recommendations")
                    st.write(
                        "1. **Monitor Performance**: Track actual performance against these projections and be ready to adjust."
                    )
                    st.write(
                        "2. **A/B Testing**: Consider running A/B tests on top-performing platforms to further optimize campaigns."
                    )
                    st.write(
                        "3. **Seasonal Adjustments**: Adjust this allocation based on seasonal trends in your industry."
                    )
                    st.write(
                        "4. **Reinvestment Strategy**: Consider reinvesting a portion of returns into the highest-performing channels."
                    )
    
    # Tab 4: Dashboard
    with tabs[3]:
        st.header("Interactive Dashboard")
        
        if st.session_state.data is not None and st.session_state.optimization_result is not None:
            # Create a dashboard with key metrics and visualizations
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_roi = st.session_state.data['ROI'].mean()
                st.metric("Average ROI", f"{avg_roi:.2f}x")
            
            with col2:
                if 'Conversion_Rate' in st.session_state.data.columns:
                    avg_conv = st.session_state.data['Conversion_Rate'].mean() * 100
                    st.metric("Avg. Conversion Rate", f"{avg_conv:.2f}%")
            
            with col3:
                if 'Acquisition_Cost' in st.session_state.data.columns:
                    avg_cpa = st.session_state.data['Acquisition_Cost'].mean()
                    st.metric("Avg. Cost Per Acquisition", f"${avg_cpa:.2f}")
            
            st.divider()
            
            # Show optimized budget allocation
            st.subheader("Optimized Budget Allocation")
            
            # Combine charts in a single row
            col1, col2 = st.columns(2)
            
            with col1:
                budget_fig = plot_budget_allocation(st.session_state.optimization_result)
                st.plotly_chart(budget_fig, use_container_width=True, key="budget_tab4")
            
            with col2:
                returns_fig = plot_expected_returns(st.session_state.optimization_result)
                st.plotly_chart(returns_fig, use_container_width=True, key="returns_tab4")
            
            # Show platform performance comparison
            st.subheader("Platform Performance Comparison")
            
            if 'Channel_Used' in st.session_state.data.columns and 'ROI' in st.session_state.data.columns:
                platform_metrics = st.session_state.processed_data.copy()
                
                # Create a radar chart for platform comparison
                categories = ['ROI', 'Conversion_Rate', 'Engagement']
                available_categories = [c for c in categories if c in platform_metrics.columns]
                
                if len(available_categories) > 1:
                    fig = go.Figure()
                    
                    for platform in platform_metrics['Channel_Used'].unique():
                        platform_data = platform_metrics[platform_metrics['Channel_Used'] == platform]
                        
                        # Normalize values between 0 and 1 for radar chart
                        values = []
                        for cat in available_categories:
                            val = platform_data[cat].values[0]
                            min_val = platform_metrics[cat].min()
                            max_val = platform_metrics[cat].max()
                            normalized = (val - min_val) / (max_val - min_val) if max_val > min_val else 0
                            values.append(normalized)
                        
                        # Add platform to radar chart
                        fig.add_trace(go.Scatterpolar(
                            r=values,
                            theta=available_categories,
                            fill='toself',
                            name=platform
                        ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 1]
                            )
                        ),
                        title="Platform Performance Comparison",
                        showlegend=True
                    )
                    
                    # In Tab 1 (Data Overview)
                    st.plotly_chart(fig, use_container_width=True, key="platform_distribution")
                    
                    # In Tab 2 (Exploratory Analysis)
                    st.plotly_chart(roi_fig, use_container_width=True, key="roi_by_platform")
                    st.plotly_chart(cpa_conv_fig, use_container_width=True, key="cpa_vs_conversion")
                    st.plotly_chart(time_fig, use_container_width=True, key="time_series")
                    
                    # In Tab 4 (Dashboard) - Radar chart
                    st.plotly_chart(fig, use_container_width=True, key="radar_chart")
        else:
            st.info("Run the budget optimizer to see the dashboard")

# End of application
