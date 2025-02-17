import pandas as pd
from typing import List, Optional
import streamlit as st

def apply_custom_style():
    """Apply custom CSS styling"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');
        * {font-family: 'Poppins', sans-serif;}
        #MainMenu, footer, .stDeployButton, #stDecoration {display: none;}
        button[title="View fullscreen"] {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def load_dashboard_data():
    """Load and prepare data for dashboard"""
    try:
        return pd.read_csv("data\internet_gdp_data.csv", index_col=0)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def create_sidebar_filters(df: pd.DataFrame):
    """Create filter widgets and information in the sidebar"""
    # Project Information Section
    st.sidebar.title("Global Internet Patterns")
    
    st.sidebar.markdown("""
        ### About the Project
        A two-decade journey through global internet adoption, revealing the stories of 
        progress, barriers, and persistent challenges (2000-2023).
        
        *This project is an entry for the DataCamp Competition: Analyzing global internet patterns*
    """)
    
    # Filters Section
    st.sidebar.markdown("---")
    st.sidebar.header("Data Filters")
    
    options = get_filter_options(df)
    
    selected_country = st.sidebar.selectbox(
        "Select Country",
        options=["All"] + options['countries'],
        help="View data for a specific country"
    )
    
    # Disable other filters if country is selected
    is_disabled = selected_country != "All"
    
    selected_region = st.sidebar.selectbox(
        "Select Region",
        options=["All"] + options['regions'],
        disabled=is_disabled,
        help="Filter by geographical region"
    )
    
    selected_income = st.sidebar.selectbox(
        "Select Income Group",
        options=["All"] + options['incomegroups'],
        disabled=is_disabled,
        help="Filter by World Bank income classification"
    )
    
    selected_growth = st.sidebar.selectbox(
        "Select Growth Category",
        options=["All"] + options['growth_categories'],
        disabled=is_disabled,
        help="Filter by internet adoption growth rate"
    )
    
    # About the Author Section
    st.sidebar.markdown("---")
    st.sidebar.header("About the Author")
    
    st.sidebar.markdown("""
        **John Paul Curada**  
        A passionate 2nd year Computer Science student at Polytechnic University 
        of the Philippines, exploring the intersection of data and technology.
        
        [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue.svg)](https://www.linkedin.com/in/jpcurada/)
        [![GitHub](https://img.shields.io/badge/GitHub-Follow-black.svg)](https://github.com/JpCurada)
    """)
    
    return {
        'country': None if selected_country == "All" else [selected_country],
        'region': None if selected_region == "All" else [selected_region],
        'income': None if selected_income == "All" else [selected_income],
        'growth': None if selected_growth == "All" else [selected_growth]
    }

def filter_data(
    df: pd.DataFrame,
    selected_countries: Optional[List[str]] = None,
    selected_incomegroups: Optional[List[str]] = None,
    selected_regions: Optional[List[str]] = None,
    selected_growth_categories: Optional[List[str]] = None,
    include_nulls: bool = False
) -> pd.DataFrame:
    """
    Filter DataFrame based on selected filters.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame
    selected_countries (list): List of selected countries
    selected_incomegroups (list): List of selected income groups
    selected_regions (list): List of selected regions
    selected_growth_categories (list): List of selected growth categories
    include_nulls (bool): Whether to include null values
    
    Returns:
    pd.DataFrame: Filtered DataFrame
    """
    filtered_df = df.copy()
    
    def apply_filter(df: pd.DataFrame, column: str, selected_values: List[str]) -> pd.DataFrame:
        if not selected_values:
            return df
        return df[df[column].isin(selected_values)]
    
    # Apply filters sequentially if selections are provided
    if selected_countries:
        filtered_df = apply_filter(filtered_df, 'country_name', selected_countries)
    elif selected_incomegroups:  # Only apply if no country is selected
        filtered_df = apply_filter(filtered_df, 'incomegroup', selected_incomegroups)
    
    if selected_regions and not selected_countries:  # Only apply if no country is selected
        filtered_df = apply_filter(filtered_df, 'region', selected_regions)
        
    if selected_growth_categories and not selected_countries:  # Only apply if no country is selected
        filtered_df = apply_filter(filtered_df, 'growth_category', selected_growth_categories)
    
    return filtered_df

def get_filter_options(df: pd.DataFrame) -> dict:
    """
    Get all available filter options from the DataFrame.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame
    
    Returns:
    dict: Dictionary containing lists of unique values for each filter category
    """
    return {
        'countries': sorted(df['country_name'].dropna().unique().tolist()),
        'incomegroups': sorted(df['incomegroup'].dropna().unique().tolist()),
        'regions': sorted(df['region'].dropna().unique().tolist()),
        'growth_categories': sorted(df['growth_category'].dropna().unique().tolist())
    }