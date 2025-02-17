from exploralytics.visualize import Visualizer
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional
from plotly.subplots import make_subplots

def get_filtered_context(region: Optional[str] = None, 
                        country: Optional[str] = None,
                        incomegroup: Optional[str] = None) -> str:
    """
    Generate context string based on applied filters.
    
    Parameters:
    region (Optional[str]): Selected region
    country (Optional[str]): Selected country
    incomegroup (Optional[str]): Selected income group
    
    Returns:
    str: Contextual string for visualization titles
    """
    if country:
        return f"in {country}"
    elif region:
        return f"in {region}"
    elif incomegroup:
        return f"in {incomegroup} Countries"
    return "Globally"

def create_internet_usage_map(df: pd.DataFrame,
                            region: Optional[str] = None,
                            country: Optional[str] = None,
                            incomegroup: Optional[str] = None) -> go.Figure:
    """
    Create a choropleth map showing percentage of population using internet by country.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing internet usage data
                      Required columns: country_code, year, internet_usage, country_name
    region (Optional[str]): Selected region for context
    country (Optional[str]): Selected country for context
    incomegroup (Optional[str]): Selected income group for context
    
    Returns:
    go.Figure: Plotly figure object with the choropleth map
    """
    # Get context for title
    context = get_filtered_context(region, country, incomegroup)
    title = f"Digital Divide {context}: Leaders and Laggards<br>" + \
            f"<sup>Two decades of internet adoption progress (2000-2023)</sup>"
    
    # Custom color scale from red to green
    colors = [
        [0, 'rgb(215,48,39)'],      # Dark red
        [0.2, 'rgb(244,109,67)'],   # Light red
        [0.4, 'rgb(253,174,97)'],   # Orange
        [0.6, 'rgb(166,217,106)'],  # Light green
        [0.8, 'rgb(102,189,99)'],   # Medium green
        [1, 'rgb(26,152,80)']       # Dark green
    ]
    
    fig = px.choropleth(
        df,
        locations="country_code",
        color="internet_usage",
        hover_name="country_name",
        animation_frame="year",
        color_continuous_scale=colors,
        range_color=[0, 100],
        title=title,
        labels={'internet_usage': 'Internet Usage'}
    )
    
    # Enhance layout for better visualization
    fig.update_layout(
        template='simple_white',
        height=768,
        width=1366,
        margin=dict(t=100, b=50, l=50, r=50),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular',
            coastlinecolor='lightgray',
            landcolor='white',
            countrycolor='lightgray'
        ),
        coloraxis_colorbar=dict(
            title=dict(
                text="Population with<br>Internet Access (%)",
                font=dict(size=14)
            ),
            ticksuffix="%",
            len=0.6,
            thickness=20,
            x=0.95
        ),
        title=dict(
            font=dict(size=20),
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        )
    )
    
    # Optimize animation settings
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
    
    # Enhanced year slider
    fig.layout.sliders[0].currentvalue = dict(
        prefix="Year: ",
        font=dict(size=16, color='darkgray'),
        visible=True,
        xanchor="right"
    )
    
    # Add hover template
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>" +
                      "Internet Usage: %{z:.1f}%<br>" +
                      "<extra></extra>"
    )
    
    return fig

def create_penetration_trend(df: pd.DataFrame,
                           region: Optional[str] = None,
                           country: Optional[str] = None,
                           incomegroup: Optional[str] = None) -> go.Figure:
    """
    Create a line chart showing internet penetration trend with historical markers.
    
    Parameters:
    df (pd.DataFrame): Filtered DataFrame containing internet usage data
                      Must have 'year' and 'internet_usage' columns
    region (Optional[str]): Selected region for context
    country (Optional[str]): Selected country for context
    incomegroup (Optional[str]): Selected income group for context
    
    Returns:
    go.Figure: Plotly figure object containing the line chart with annotations
    """
    # Group by year and calculate mean penetration
    yearly_avg = df.groupby('year')['internet_usage'].mean().reset_index()
    
    # Get context for title
    context = get_filtered_context(region, country, incomegroup)
    title = f"How did global milestones reshape the digital journey {context}?<br>" + \
            f"<sup>Tracing the impact of social media, technological advances, and global crises on internet adoption (2000-2023)</sup>"
    
    # Create line chart
    fig = px.line(
        yearly_avg,
        x='year',
        y='internet_usage',
        title=title,
        labels={
            'internet_usage': 'Average Penetration Rate (%)',
            'year': 'Year'
        }
    )
    
    # Update layout with shapes and annotations
    fig.update_layout(
        template='simple_white',
        title=dict(
            font=dict(size=20),
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        height=400,
        xaxis_title='Year',
        yaxis_title='Penetration Rate (%)',
        yaxis_range=[0, 100],
        showlegend=False,
        shapes=[
            # Facebook Launch Line
            dict(
                type='line',
                x0=2004,
                x1=2004,
                y0=0,
                y1=100,
                line=dict(
                    color='#3b5998',
                    width=2,
                    dash='dash'
                )
            ),
            # 4G Launch Line
            dict(
                type='line',
                x0=2009,
                x1=2009,
                y0=0,
                y1=100,
                line=dict(
                    color='#00539C',
                    width=2,
                    dash='dash'
                )
            ),
            # COVID-19 Period Rectangle
            dict(
                type='rect',
                x0=2019,
                x1=2023,
                y0=0,
                y1=100,
                fillcolor='red',
                opacity=0.1,
                line_width=0,
                layer='below'
            )
        ],
        annotations=[
            dict(
                x=2004,
                y=95,
                text="Facebook Launch",
                showarrow=False,
                font=dict(color="#3b5998")
            ),
            dict(
                x=2009,
                y=90,
                text="4G Launch",
                showarrow=False,
                font=dict(color="#00539C")
            ),
            dict(
                x=2021,
                y=85,
                text="COVID-19 Period",
                showarrow=False,
                font=dict(color="red")
            )
        ]
    )
    
    # Update line properties
    fig.update_traces(
        line_color='#94C973',
        line_width=2
    )
    
    return fig

def create_gdp_internet_scatter(df: pd.DataFrame,
                              region: Optional[str] = None,
                              country: Optional[str] = None,
                              incomegroup: Optional[str] = None) -> go.Figure:
    """
    Create a scatter plot showing internet usage vs GDP trend across years.
    
    Parameters:
    df (pd.DataFrame): Filtered DataFrame containing internet usage and GDP data
                      Required columns: year, internet_usage, gdp_per_capita
    region (Optional[str]): Selected region for context
    country (Optional[str]): Selected country for context
    incomegroup (Optional[str]): Selected income group for context
    
    Returns:
    go.Figure: Plotly figure object with scatter plot and trendline
    """
    # Ensure one point per year by averaging if multiple countries are selected
    yearly_data = df.groupby('year').agg({
        'internet_usage': 'mean',
        'gdp_per_capita': 'mean'
    }).reset_index()
    
    # Get context for title
    context = get_filtered_context(region, country, incomegroup)
    title = f"Economic Prosperity and Digital Access {context}<br>" + \
            f"<sup>The relationship between GDP per capita and internet penetration (2000-2023)</sup>"

    # Create scatter plot
    fig = px.scatter(
        yearly_data,
        x='gdp_per_capita',
        y='internet_usage',
        text='year',
        trendline="ols",
        title=title,
        labels={
            'gdp_per_capita': 'GDP per Capita (current US$)',
            'internet_usage': 'Internet Usage (%)',
            'year': 'Year'
        }
    )
    
    # Update layout
    fig.update_layout(
        template='simple_white',
        height=500,
        showlegend=False,
        xaxis=dict(
            title_font=dict(size=12),
            tickfont=dict(size=10),
            gridcolor='lightgray',
            type='log'  # Add log scale for GDP
        ),
        yaxis=dict(
            title_font=dict(size=12),
            tickfont=dict(size=10),
            gridcolor='lightgray',
            range=[0, 100]
        ),
        title=dict(
            font=dict(size=20),
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        hovermode='x unified'
    )
    
    # Update markers and hover info
    fig.update_traces(
        marker=dict(
            size=12,
            color='#94C973',
            line=dict(width=1, color='DarkSlateGrey')
        ),
        textposition='top center',
        hovertemplate="<br>".join([
            "Year: %{text}",
            "GDP per Capita: $%{x:,.2f}",
            "Internet Usage: %{y:.1f}%",
            "<extra></extra>"
        ]),
        selector=dict(mode='markers+text')
    )
    
    return fig

def create_region_data_subplot(df: pd.DataFrame,
                          region: Optional[str] = None,
                          country: Optional[str] = None,
                          incomegroup: Optional[str] = None) -> go.Figure:
    """
    Create a subplot with regional internet penetration and low-connectivity countries.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing internet usage data
    region (Optional[str]): Selected region for context
    incomegroup (Optional[str]): Selected income group for context
    
    Returns:
    go.Figure: Plotly figure with two subplots
    """
    # Create figure with subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Regional Internet Penetration (2023)',
                       'Countries with <50% Internet Access'),
        column_widths=[0.6, 0.4],
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Get 2023 data
    latest_data = df[df['year'] == 2023]
    
    # Left subplot: Regional averages
    region_avg = latest_data.groupby('region')['internet_usage'].mean().sort_values(ascending=True)
    
    fig.add_trace(
        go.Bar(
            x=region_avg.values,
            y=region_avg.index,
            orientation='h',
            marker_color='#94C973',
            text=[f'{x:.1f}%' for x in region_avg.values],
            textposition='auto',
            name='Regional Penetration'
        ),
        row=1, col=1
    )
    
    # Right subplot: Low connectivity countries by region
    low_connectivity = latest_data[latest_data['internet_usage'] < 50]
    low_by_region = low_connectivity.groupby('region').size().sort_values(ascending=True)
    
    # Add percentage of total countries in each region
    total_by_region = latest_data.groupby('region').size()
    percentages = (low_by_region / total_by_region * 100).round(1)
    
    hover_text = [f"{count} countries<br>({pct}% of region)" 
                 for count, pct in zip(low_by_region.values, percentages.values)]
    
    fig.add_trace(
        go.Bar(
            x=low_by_region.values,
            y=low_by_region.index,
            orientation='h',
            marker_color='#FF9999',
            text=hover_text,
            textposition='auto',
            name='Low Connectivity'
        ),
        row=1, col=2
    )
    
    # Update layout based on context
    context = get_filtered_context(region, country, incomegroup)
    title = f"Regional Internet Penetration and Digital Inclusion Challenges {context}"
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title=dict(
            text=title,
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        template='simple_white'
    )
    
    # Update axes
    fig.update_xaxes(title_text='Penetration Rate (%)', row=1, col=1)
    fig.update_xaxes(title_text='Number of Countries', row=1, col=2)
    
    # Update yaxis for better readability
    fig.update_yaxes(title_text='', row=1, col=1)
    fig.update_yaxes(title_text='', row=1, col=2)
    
    return fig