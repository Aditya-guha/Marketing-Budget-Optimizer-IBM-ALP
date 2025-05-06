import pandas as pd
import numpy as np

def validate_data(data):
    """
    Validate that the uploaded data has the required columns
    """
    required_columns = ['Channel_Used', 'ROI']
    recommended_columns = ['Conversion_Rate', 'Acquisition_Cost', 'Clicks', 'Impressions']
    
    missing_required = [col for col in required_columns if col not in data.columns]
    
    if missing_required:
        return {
            "valid": False,
            "message": f"Missing required columns: {', '.join(missing_required)}"
        }
    
    missing_recommended = [col for col in recommended_columns if col not in data.columns]
    
    if missing_recommended:
        message = f"Data is valid but missing recommended columns: {', '.join(missing_recommended)}"
    else:
        message = "All required and recommended columns are present"
    
    return {
        "valid": True,
        "message": message
    }

def process_data(data):
    """
    Process and aggregate data for optimization
    """
    # Ensure we have the required columns
    if 'Channel_Used' not in data.columns or 'ROI' not in data.columns:
        raise ValueError("Data must contain 'Channel_Used' and 'ROI' columns")
    
    # Convert numeric columns to float, coercing errors to NaN
    numeric_columns = ['ROI', 'Conversion_Rate', 'Acquisition_Cost', 'Clicks', 'Impressions']
    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # Group by platform and calculate average metrics
    grouped = data.groupby('Channel_Used').agg({
        'ROI': 'mean',
        'Conversion_Rate': 'mean' if 'Conversion_Rate' in data.columns else None,
        'Acquisition_Cost': 'mean' if 'Acquisition_Cost' in data.columns else None,
        'Clicks': 'sum' if 'Clicks' in data.columns else None,
        'Impressions': 'sum' if 'Impressions' in data.columns else None
    }).reset_index()
    
    # Drop None columns (from optional metrics)
    grouped = grouped.dropna(axis=1)
    
    # Calculate engagement if possible
    if 'Clicks' in grouped.columns and 'Impressions' in grouped.columns:
        grouped['Engagement'] = grouped['Clicks'] / grouped['Impressions']
    
    return grouped