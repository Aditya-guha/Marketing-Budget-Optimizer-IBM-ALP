import pandas as pd
import numpy as np
from scipy.optimize import linprog

def optimize_budget(platform_data, total_budget):
    """
    Use linear programming to optimize budget allocation across platforms
    to maximize expected ROI
    
    Args:
        platform_data: DataFrame with platform performance metrics
        total_budget: Total budget to allocate
        
    Returns:
        DataFrame with optimized budget allocation
    """
    # Extract platforms and their ROIs
    platforms = platform_data['Channel_Used'].values
    rois = platform_data['ROI'].values
    
    # Objective function: Maximize ROI (linprog minimizes, so negate ROI)
    c = -rois
    
    # Constraints:
    # 1. Sum of budgets = total_budget
    A_eq = np.ones((1, len(platforms)))
    b_eq = np.array([total_budget])
    
    # 2. Budget for each platform >= 0
    bounds = [(0, None) for _ in range(len(platforms))]
    
    # Solve the linear programming problem
    result = linprog(
        c=c,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method='highs'
    )
    
    if not result.success:
        raise ValueError(f"Optimization failed: {result.message}")
    
    # Create result DataFrame
    allocation = result.x
    expected_returns = allocation * rois
    
    result_df = pd.DataFrame({
        'Platform': platforms,
        'ROI': rois,
        'Budget_Allocation': allocation,
        'Expected_Return': expected_returns,
        'Allocation_Percentage': (allocation / total_budget) * 100
    })
    
    # Sort by expected return (descending)
    result_df = result_df.sort_values('Expected_Return', ascending=False).reset_index(drop=True)
    
    # Format numeric columns
    result_df['Budget_Allocation'] = result_df['Budget_Allocation'].round(2)
    result_df['Expected_Return'] = result_df['Expected_Return'].round(2)
    result_df['Allocation_Percentage'] = result_df['Allocation_Percentage'].round(2)
    
    return result_df