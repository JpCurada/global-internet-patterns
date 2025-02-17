import streamlit as st
from utils import (filter_data, 
                   load_dashboard_data,
                   apply_custom_style,
                   create_sidebar_filters
                   )

from visuals import (create_penetration_trend, 
                     create_internet_usage_map,
                     create_gdp_internet_scatter,
                     create_region_data_subplot
                     )
import pandas as pd

# Page configuration
st.set_page_config(
    page_title='Internet Usage Dashboard',
    layout='wide'
)

# Apply custom styling
apply_custom_style()

# Main content
st.header("Who's connected? Two decade story of our digital world", divider='grey')
st.caption("Data source: DataCamp & World Bank")

# Load data
df = load_dashboard_data()

if not df.empty:
    # Create sidebar filters
    filters = create_sidebar_filters(df)
    
    # Apply filters
    filtered_df = filter_data(
        df,
        selected_countries=filters['country'],
        selected_incomegroups=filters['income'],
        selected_regions=filters['region'],
        selected_growth_categories=filters['growth']
    )
    
    # Display filtered data
    if not filtered_df.empty:
        # Calculate dynamic metrics
        filtered_df_2023 = filtered_df[filtered_df['year'] == 2023]
        region_averages = filtered_df_2023.groupby('region')['internet_usage'].mean().round(1)
        top_region = region_averages.idxmax()
        top_region_value = region_averages.max()

        # Get top performers
        top_countries = filtered_df_2023.nlargest(3, 'internet_usage')
        top_countries_text = ", ".join(
            f"{country} ({value:.1f}%)" 
            for country, value in zip(top_countries['country_name'], top_countries['internet_usage'])
        )

        # Initial narrative based on filters
        if filters['region']:
            selected_region = filters['region'][0]
            region_avg = region_averages.get(selected_region, 0)
            st.write(f"""
                The digital transformation journey reveals an interesting story in {selected_region}. 
                With an average internet penetration rate of {region_avg}% in 2023, this region shows 
                {'remarkable progress' if region_avg > 50 else 'ongoing development'} in digital connectivity. 
                For context, {top_region} leads globally with {top_region_value}% average penetration.
            """)
        elif filters['country']:
            country_name = filters['country'][0]
            country_data = filtered_df_2023[filtered_df_2023['country_name'] == country_name].iloc[0]
            st.write(f"""
                In {country_name}'s digital journey, we see a country that has reached {country_data['internet_usage']:.1f}% 
                internet penetration by 2023. As part of {country_data['region']}, and classified as a {country_data['incomegroup']} country, 
                this represents {'significant achievement' if country_data['internet_usage'] > 80 else 'ongoing progress'} 
                in digital inclusion.
            """)
        elif filters['income']:
            incomegroup = filters['income'][0]
            income_data = filtered_df_2023[filtered_df_2023['incomegroup'] == incomegroup]
            avg_penetration = income_data['internet_usage'].mean()
            st.write(f"""
                Looking at {incomegroup} economies, we observe an average internet penetration of {avg_penetration:.1f}% in 2023. 
                This economic group faces {'substantial advantages' if avg_penetration > 70 else 'unique challenges'} 
                in expanding digital access. The global leaders in this category include {top_countries_text}.
            """)
        else:
            st.write(f"""
                The global digital landscape shows remarkable variation in internet adoption. While {top_region} 
                leads with {top_region_value}% average penetration, the story varies significantly across regions 
                and economic groups. The global leaders in internet adoption are {top_countries_text}, 
                showcasing what's possible in digital connectivity.
            """)

        # Display choropleth map
        fig_map = create_internet_usage_map(
            filtered_df,
            region=filters['region'][0] if filters['region'] else None,
            country=filters['country'][0] if filters['country'] else None,
            incomegroup=filters['income'][0] if filters['income'] else None
        )
        st.plotly_chart(fig_map, use_container_width=True)

        # Calculate key metrics for map narrative
        latest_year = filtered_df['year'].max()
        latest_data = filtered_df[filtered_df['year'] == latest_year]
        high_penetration = latest_data[latest_data['internet_usage'] >= 80]['country_name'].count()
        low_penetration = latest_data[latest_data['internet_usage'] <= 20]['country_name'].count()
        global_average = latest_data['internet_usage'].mean()
        growth_data = filtered_df.groupby('country_name')['yoy_growth'].mean().nlargest(3)
        fastest_growing = ", ".join([f"{country}" for country in growth_data.index])

        # Map narrative
        map_context = ''
        if filters['region']:
            region_avg = region_averages.get(selected_region, 0)
            map_context = f"Within {selected_region}, we see varying levels of progress, averaging {region_avg}% penetration"
        elif filters['country']:
            map_context = f"Examining {country_name}'s position in the global context"
        elif filters['income']:
            map_context = f"Among {incomegroup} economies, we observe distinct patterns of digital adoption"
        else:
            map_context = "Globally, we observe stark contrasts in internet adoption patterns"

        st.write(f"""
            The visualization above illustrates the digital transformation from 2000 to {latest_year}. {map_context}, 
            with {high_penetration} countries achieving over 80% internet penetration, while {low_penetration} countries 
            remain below 20%.

            The average penetration of {global_average:.1f}% masks significant disparities. Countries like {fastest_growing} 
            demonstrate how rapid digital transformation is possible with effective policies and infrastructure investments.
        """)

        # Always use unfiltered data for the regional subplot
        df_full = load_dashboard_data()  # Get original unfiltered data
        fig_region = create_region_data_subplot(df_full)  # Create subplot with full dataset
        st.plotly_chart(fig_region, use_container_width=True)

        # Calculate metrics for narrative using full dataset
        latest_data_full = df_full[df_full['year'] == 2023]
        low_connectivity = latest_data_full[latest_data_full['internet_usage'] < 50]

        # Get highest and lowest regions from full dataset
        highest_region = latest_data_full.groupby('region')['internet_usage'].mean().idxmax()
        lowest_region = latest_data_full.groupby('region')['internet_usage'].mean().idxmin()
        highest_avg = latest_data_full.groupby('region')['internet_usage'].mean().max()
        lowest_avg = latest_data_full.groupby('region')['internet_usage'].mean().min()

        # Calculate region with most low-connectivity countries
        most_challenging_region = low_connectivity.groupby('region').size().idxmax()
        challenge_count = low_connectivity.groupby('region').size().max()

        # Dynamic narrative based on filters
        if filters['region']:
            selected_region = filters['region'][0]
            region_avg = latest_data_full[latest_data_full['region'] == selected_region]['internet_usage'].mean()
            region_low = len(low_connectivity[low_connectivity['region'] == selected_region])
            total_in_region = len(latest_data_full[latest_data_full['region'] == selected_region])
            
            st.write(f"""
                Looking at {selected_region}, we see an average penetration of {region_avg:.1f}% against the broader regional landscape. 
                Within this region, {region_low} out of {total_in_region} countries have less than 50% internet penetration. 
                This regional view helps contextualize the digital development challenges and opportunities across different 
                parts of the world.
            """)
        elif filters['country']:
            country_data = latest_data_full[latest_data_full['country_name'] == filters['country'][0]]
            if not country_data.empty:
                country_region = country_data.iloc[0]['region']
                region_avg = latest_data_full[latest_data_full['region'] == country_region]['internet_usage'].mean()
                region_low = len(low_connectivity[low_connectivity['region'] == country_region])
                
                st.write(f"""
                    While examining {filters['country'][0]}, we can see it's part of {country_region}, 
                    where the regional average stands at {region_avg:.1f}%. This region has {region_low} countries 
                    with less than 50% internet penetration, showing the broader regional context of digital adoption challenges.
                """)
        elif filters['income']:
            income_group = filters['income'][0]
            income_regions = latest_data_full[latest_data_full['income_group'] == income_group]['region'].unique()
            region_stats = [f"{r} ({latest_data_full[latest_data_full['region'] == r]['internet_usage'].mean():.1f}%)"
                        for r in income_regions]
            
            st.write(f"""
                For {income_group} economies, the regional distribution shown above provides important context. 
                These economies span multiple regions, including {', '.join(region_stats)}, demonstrating how 
                economic classification intersects with regional digital development patterns.
            """)
        else:
            st.write(f"""
                The regional comparison reveals stark contrasts in digital inclusion. {highest_region} leads with 
                an average penetration of {highest_avg:.1f}%, while {lowest_region} shows the lowest regional average 
                at {lowest_avg:.1f}%. {most_challenging_region} faces particular challenges, with {challenge_count} countries 
                still below 50% internet penetration, highlighting where focused digital development efforts may be most needed.
            """)

        # Display trend line
        fig_trend = create_penetration_trend(
            filtered_df,
            region=filters['region'][0] if filters['region'] else None,
            country=filters['country'][0] if filters['country'] else None,
            incomegroup=filters['income'][0] if filters['income'] else None
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # Timeline narrative
        timeline_context = ''
        if filters['region']:
            timeline_context = f"In {selected_region}"
        elif filters['country']:
            timeline_context = f"In {country_name}"
        elif filters['income']:
            timeline_context = f"Among {incomegroup} economies"
        else:
            timeline_context = "Globally"

        st.write(f"""
            {timeline_context}, the digital journey has been shaped by key milestones. The launch of Facebook in 2004 
            marked the beginning of social media's influence on internet adoption. The introduction of 4G technology 
            in 2009 brought faster, more reliable connectivity, particularly benefiting areas without traditional infrastructure.

            The COVID-19 pandemic (2019-2023) then triggered unprecedented changes, as remote work and digital services 
            became essential. This period saw {'remarkable acceleration' if filters.get('growth') == ['High Growth'] 
            else 'steady progress'} in digital transformation, though the impact varied across different contexts.
        """)

        # Display scatter plot
        fig_scatter = create_gdp_internet_scatter(
            filtered_df,
            region=filters['region'][0] if filters['region'] else None,
            country=filters['country'][0] if filters['country'] else None,
            incomegroup=filters['income'][0] if filters['income'] else None
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Calculate correlation and GDP statistics
        correlation = filtered_df[['gdp_per_capita', 'internet_usage']].corr().iloc[0,1]
        high_gdp_countries = filtered_df[
            (filtered_df['year'] == latest_year) & 
            (filtered_df['gdp_per_capita'] >= filtered_df['gdp_per_capita'].quantile(0.9))
        ]['country_name'].tolist()
        high_gdp_text = ", ".join(high_gdp_countries[:3])

        # GDP-Internet relationship narrative
        gdp_context = ''
        if filters['region']:
            gdp_context = f"In {selected_region}, this relationship"
        elif filters['country']:
            gdp_context = f"For {country_name}, this pattern"
        elif filters['income']:
            gdp_context = f"Among {incomegroup} economies, this correlation"
        else:
            gdp_context = "This global relationship"

        st.write(f"""
            The economic dimension of internet adoption shows a correlation of {correlation:.2f}. {gdp_context} 
            reveals how GDP per capita influences digital access. Notable examples include {high_gdp_text}, 
            where economic strength supports high internet penetration.

            However, some regions achieve higher than expected internet adoption despite economic constraints, 
            demonstrating how effective policies and focused infrastructure investments can help bridge the 
            digital divide. This suggests that while economic resources matter, they're not the sole determinant 
            of digital inclusion.
        """)

    else:
        st.info("No data matches the selected filters. Please adjust your selection.")

        