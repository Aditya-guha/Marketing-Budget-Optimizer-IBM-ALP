import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_roi_by_platform(data):
    """
    Create a bar chart showing ROI by platform
    """
    fig = px.bar(
        data,
        x='Channel_Used',
        y='ROI',
        title='Return on Investment (ROI) by Platform',
        color='ROI',
        color_continuous_scale='Viridis',
        labels={'Channel_Used': 'Platform', 'ROI': 'Return on Investment'}
    )
    
    fig.update_layout(
        xaxis_title='Platform',
        yaxis_title='ROI',
        coloraxis_showscale=False
    )
    
    return fig

def plot_cpa_vs_conversion(data):
    """
    Create a scatter plot of CPA vs Conversion Rate
    """
    if 'Acquisition_Cost' not in data.columns or 'Conversion_Rate' not in data.columns:
        # Create empty figure with message if data is missing
        fig = go.Figure()
        fig.add_annotation(
            text="Missing required data (Acquisition_Cost or Conversion_Rate)",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    fig = px.scatter(
        data,
        x='Conversion_Rate',
        y='Acquisition_Cost',
        color='ROI',
        size='ROI',
        hover_name='Channel_Used',
        title='Cost Per Acquisition vs Conversion Rate',
        labels={
            'Conversion_Rate': 'Conversion Rate',
            'Acquisition_Cost': 'Cost Per Acquisition ($)',
            'ROI': 'Return on Investment'
        }
    )
    
    fig.update_layout(
        xaxis_title='Conversion Rate',
        yaxis_title='Cost Per Acquisition ($)'
    )
    
    return fig

def plot_time_series(data, metric):
    """
    Create a time series plot for the selected metric
    """
    if 'Date' not in data.columns or metric not in data.columns:
        # Create empty figure with message if data is missing
        fig = go.Figure()
        fig.add_annotation(
            text=f"Missing required data (Date or {metric})",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Group by date and platform
    time_data = data.groupby(['Date', 'Channel_Used'])[metric].mean().reset_index()
    
    fig = px.line(
        time_data,
        x='Date',
        y=metric,
        color='Channel_Used',
        title=f'{metric} Over Time by Platform',
        labels={'Date': 'Date', metric: metric, 'Channel_Used': 'Platform'}
    )
    
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title=metric
    )
    
    return fig

def plot_budget_allocation(result_df):
    """
    Create a bar chart showing budget allocation by platform
    """
    fig = px.bar(
        result_df,
        x='Platform',
        y='Budget_Allocation',
        title='Optimized Budget Allocation by Platform',
        color='ROI',
        color_continuous_scale='Viridis',
        labels={
            'Platform': 'Platform',
            'Budget_Allocation': 'Budget Allocation ($)',
            'ROI': 'Return on Investment'
        },
        text='Allocation_Percentage'
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    
    fig.update_layout(
        xaxis_title='Platform',
        yaxis_title='Budget Allocation ($)'
    )
    
    return fig

def plot_expected_returns(result_df):
    """
    Create a bar chart showing expected returns by platform
    """
    fig = px.bar(
        result_df,
        x='Platform',
        y='Expected_Return',
        title='Expected Returns by Platform',
        color='ROI',
        color_continuous_scale='Viridis',
        labels={
            'Platform': 'Platform',
            'Expected_Return': 'Expected Return ($)',
            'ROI': 'Return on Investment'
        }
    )
    
    fig.update_layout(
        xaxis_title='Platform',
        yaxis_title='Expected Return ($)'
    )
    
    return fig