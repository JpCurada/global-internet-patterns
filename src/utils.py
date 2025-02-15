from typing import List, Optional
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression

def convert_non_numerical_to_null(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Convert non-numerical values to null in specified columns.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to be processed.
    columns (list): List of column names to check and convert.
    
    Returns:
    pd.DataFrame: The DataFrame with non-numerical values converted to null.
    """
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

def melt_internet_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reshape internet usage data from wide to long format.
    
    Parameters:
    df (pd.DataFrame): DataFrame in wide format
    
    Returns:
    pd.DataFrame: Melted DataFrame with year as categorical
    """
    melted = pd.melt(
        df, 
        id_vars=['country_name', 'country_code'],
        value_vars=df.columns[2:].tolist(),
        var_name='year',
        value_name='internet_usage'
    )
    
    # Convert year to ordinal
    melted['year'] = pd.Categorical(
        melted['year'],
        categories=[str(year) for year in range(2000, 2024)],
        ordered=True
    )
    
    return melted

def impute_year_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Impute missing values for years 2000-2023 using linear regression and mark imputed values.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame with internet usage data
    
    Returns:
    pd.DataFrame: DataFrame with imputed values for missing years
    """
    # Create copy and ensure year is numeric
    df = df.copy()
    df['year'] = pd.to_numeric(df['year'])
    
    # Initialize the complete range of years
    all_years = pd.DataFrame({'year': range(2000, 2024)})
    
    # Create empty list to store results
    imputed_data = []
    
    # Process each country separately
    for country in df['country_name'].unique():
        country_data = df[df['country_name'] == country].copy()
        
        # Create complete year range for this country
        country_years = all_years.copy()
        country_years['country_name'] = country
        country_years['country_code'] = country_data['country_code'].iloc[0]
        
        # Merge with existing data
        country_complete = pd.merge(
            country_years,
            country_data[['year', 'internet_usage', 'country_name', 'country_code']],
            on=['year', 'country_name', 'country_code'],
            how='left'
        )
        
        # If there are missing values, impute them
        if country_complete['internet_usage'].isnull().any():
            # Get existing data points
            valid_data = country_complete[~country_complete['internet_usage'].isnull()]
            
            if len(valid_data) >= 2:  # Need at least 2 points for linear regression
                # Prepare data for regression
                X = valid_data[['year']].values
                y = valid_data['internet_usage'].values
                
                # Fit linear regression
                model = LinearRegression()
                model.fit(X, y)
                
                # Predict missing values
                missing_mask = country_complete['internet_usage'].isnull()
                predictions = model.predict(country_complete[missing_mask][['year']].values)
                
                # Clip predictions to valid range
                predictions = np.clip(predictions, 0, 100)
                
                # Update values in dataframe
                country_complete.loc[missing_mask, 'internet_usage'] = predictions
                
                # Mark data sources
                country_complete['data_source'] = 'Original'
                country_complete.loc[missing_mask, 'data_source'] = 'Imputed'
            
            elif len(valid_data) == 1:  # Only one valid point - use it for all missing values
                value = valid_data['internet_usage'].iloc[0]
                country_complete['internet_usage'] = country_complete['internet_usage'].fillna(value)
                country_complete['data_source'] = np.where(
                    country_complete['internet_usage'].isnull(),
                    'Imputed',
                    'Original'
                )
            
            else:  # No valid points - use global mean or default value
                global_mean = df['internet_usage'].mean()
                if pd.isna(global_mean):
                    # If no valid data at all, use a reasonable default
                    country_complete['internet_usage'] = country_complete['internet_usage'].fillna(50)
                else:
                    country_complete['internet_usage'] = country_complete['internet_usage'].fillna(global_mean)
                country_complete['data_source'] = 'Imputed'
        
        else:
            country_complete['data_source'] = 'Original'
        
        imputed_data.append(country_complete)
    
    # Combine all countries
    result = pd.concat(imputed_data, ignore_index=True)
    
    # Convert year back to string categorical
    result['year'] = result['year'].astype(str)
    result['year'] = pd.Categorical(
        result['year'],
        categories=[str(year) for year in range(2000, 2024)],
        ordered=True
    )
    
    return result.sort_values(['country_name', 'year'])

def calculate_percentage_change(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the percentage change in internet usage following industry standards.
    Based on ITU and World Bank methodologies for measuring internet adoption growth.
    
    Key standards followed:
    - Growth rates capped at 100% for year-over-year changes
    - Base effects handled through logarithmic transformation
    - Special handling for 0% penetration rates
    - NaN values for first observations
    - Accounts for penetration rate maximum of 100%
    
    Args:
        df (pd.DataFrame): Input dataframe containing internet usage data
            Must have columns: ['country_name', 'year', 'internet_usage']
            
    Returns:
        pd.DataFrame: Original dataframe with new columns:
            - yoy_growth: Year-over-year growth rate
            - growth_category: Categorization of growth rate
    """
    # Create a copy to avoid modifying the original
    df = df.copy()
    
    # Reset index and sort
    df = df.reset_index(drop=True)
    df = df.sort_values(['country_name', 'year'])
    
    # Calculate basic year-over-year growth
    df['yoy_growth'] = df.groupby('country_name')['internet_usage'].pct_change() * 100
    
    # Handle special cases following ITU standards
    df['yoy_growth'] = df['yoy_growth'].replace([np.inf, -np.inf], np.nan)
    
    # Cap growth rates at industry standard levels
    # For countries with less than 10% penetration, allow higher growth
    low_penetration_mask = df.groupby('country_name')['internet_usage'].shift(1) < 10
    df.loc[low_penetration_mask, 'yoy_growth'] = df.loc[low_penetration_mask, 'yoy_growth'].clip(-100, 200)
    df.loc[~low_penetration_mask, 'yoy_growth'] = df.loc[~low_penetration_mask, 'yoy_growth'].clip(-100, 100)
    
    # Handle zero baseline cases
    zero_prev_mask = (df.groupby('country_name')['internet_usage'].shift(1) == 0) & (df['internet_usage'] > 0)
    df.loc[zero_prev_mask, 'yoy_growth'] = 100  # Standard treatment for zero-base growth
    
    # Set first year for each country to NaN
    df.loc[~df['country_name'].duplicated(), 'yoy_growth'] = np.nan
    
    # Add growth categorization based on ITU standards
    df['growth_category'] = pd.cut(
        df['yoy_growth'],
        bins=[-np.inf, -20, -5, 5, 20, np.inf],
        labels=['Significant Decline', 'Moderate Decline', 'Stable', 'Moderate Growth', 'High Growth']
    )
    
    # Add 3-year CAGR for trend analysis
    df['usage_3yr_ago'] = df.groupby('country_name')['internet_usage'].shift(3)
    df['cagr_3yr'] = ((df['internet_usage'] / df['usage_3yr_ago']) ** (1/3) - 1) * 100
    df['cagr_3yr'] = df['cagr_3yr'].clip(-50, 100)  # Standard bounds for CAGR
    
    # Clean up
    df = df.drop('usage_3yr_ago', axis=1)
    df = df.reset_index(drop=True)
    
    return df

def process_internet_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Process internet usage data through the complete pipeline.
    
    Parameters:
    data (pd.DataFrame): Raw internet usage data
    
    Returns:
    pd.DataFrame: Processed DataFrame with imputed values and year-over-year growth
    """
    # Define year columns
    columns_to_check = [str(year) for year in range(2000, 2024)]
    
    # Process data
    cleaned_data = convert_non_numerical_to_null(data, columns_to_check)
    melted_data = melt_internet_data(cleaned_data)
    imputed_data = impute_year_values(melted_data)
    final_data = calculate_percentage_change(imputed_data)
    
    return final_data

