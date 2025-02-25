import numpy as np
import pandas as pd
from typing import Union, Sequence


def robust_trapz(y: Union[Sequence, np.ndarray, pd.Series], 
                 x: Union[Sequence, np.ndarray, pd.Series] = None,
                 dx: float = 1.0) -> float:
    """
    Calculate the area under the curve using trapezoidal integration.
    Handles edge cases similar to numpy's trapz function.
    
    Parameters:
    -----------
    y : array_like
        The y-coordinates (signal intensity values)
    x : array_like, optional
        The x-coordinates (time points). If None, dx is used as spacing.
    dx : float, optional
        The spacing between x-coordinates if x is None. Default is 1.0.
    
    Returns:
    --------
    float
        The area under the curve
        
    Edge cases handled:
    - Empty arrays
    - Single point arrays
    - NaN or inf values
    - Mismatched lengths of x and y
    - Non-monotonic x values
    """
    # Convert inputs to numpy arrays for consistent handling
    y_array = np.asarray(y, dtype=float)
    
    # Handle empty arrays
    if y_array.size == 0:
        return 0.0
    
    # Handle single point arrays
    if y_array.size == 1:
        return 0.0
    
    # Handle x coordinates
    if x is None:
        # If x is not provided, create evenly spaced points using dx
        x_array = np.arange(y_array.size) * dx
    else:
        # Convert x to numpy array
        x_array = np.asarray(x, dtype=float)
        
        # Check if lengths match
        if x_array.size != y_array.size:
            raise ValueError(f"x and y must have the same length. Got x: {x_array.size}, y: {y_array.size}")
    
    # Check if x is monotonically increasing
    if not np.all(np.diff(x_array) > 0):
        # Sort x and y if x is not monotonic
        sort_indices = np.argsort(x_array)
        x_array = x_array[sort_indices]
        y_array = y_array[sort_indices]
    
    # Handle NaN or inf values by masking them
    valid_mask = np.isfinite(x_array) & np.isfinite(y_array)
    if not np.all(valid_mask):
        x_array = x_array[valid_mask]
        y_array = y_array[valid_mask]
        
        # If we don't have enough points after filtering, return 0
        if x_array.size <= 1:
            return 0.0
    
    # Calculate width of each trapezoid
    widths = np.diff(x_array)
    
    # Calculate average heights
    avg_heights = (y_array[:-1] + y_array[1:]) / 2.0
    
    # Calculate area
    area = np.sum(avg_heights * widths)
    
    return area


# Example function to apply to multiple wells in a DataFrame
def calculate_auc(data: pd.DataFrame, time_points: Union[np.ndarray, pd.Series]) -> pd.Series:
    """
    Calculate area under the curve for each row (well) in the DataFrame
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame where each row represents a well's time series data
    time_points : array_like
        The x-coordinates (time points)
    
    Returns:
    --------
    pd.Series
        Series containing the AUC value for each well
    """
    return pd.Series({
        well: robust_trapz(y=data.loc[well], x=time_points)
        for well in data.index
    })


# Example usage
if __name__ == "__main__":
    # Create sample data
    times = np.array([0, 1, 2, 3, 4, 5])
    values = np.array([0, 1, 3, 2, 4, 3])
    
    # Calculate using our function
    our_result = robust_trapz(values, times)
    
    # Compare with numpy's trapz
    np_result = np.trapz(values, times)
    
    print(f"Our implementation: {our_result}")
    print(f"NumPy's trapz:      {np_result}")
    print(f"Difference:         {our_result - np_result}")
    
    # Test edge cases
    print("\nEdge Cases:")
    print(f"Empty array:         {robust_trapz([], [])}")
    print(f"Single point:        {robust_trapz([5], [10])}")
    print(f"With NaN values:     {robust_trapz([1, np.nan, 3, 4], [0, 1, 2, 3])}")
    print(f"Non-monotonic x:     {robust_trapz([1, 2, 3, 4], [0, 2, 1, 3])}")
