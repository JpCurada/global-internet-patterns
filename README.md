# Who's connected? Two decade story of our digital world

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://global-internet-patterns.streamlit.app/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue.svg)](https://www.linkedin.com/in/jpcurada/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black.svg)](https://github.com/JpCurada)

## About the Project

A data-driven exploration of global internet adoption from 2000 to 2023, revealing the stories of digital progress, barriers, and persistent challenges across different regions and economic groups. This interactive dashboard provides insights into how internet access has evolved globally, highlighting both achievements and areas needing attention.

This project is my entry for the [DataCamp Competition: Analyzing Global Internet Patterns](https://www.datacamp.com/datalab/w/517a04fb-a922-4754-b181-68724be62c47).

### Key Features

1. **Interactive World Map**
   - Animated choropleth visualization showing internet penetration rates
   - Year-by-year progression from 2000 to 2023
   - Color-coded representation of digital divide

2. **Regional Analysis Dashboard**
   - Comparative view of internet adoption across regions
   - Identification of areas with low connectivity
   - Progress tracking over time

3. **Economic Impact Analysis**
   - GDP vs. Internet penetration correlation
   - Income group comparisons
   - Development trajectory visualization

4. **Timeline Visualization**
   - Major technological milestones
   - Impact of global events (e.g., COVID-19)
   - Growth rate analysis

### Data Filters

The dashboard offers several filtering options to explore the data:

1. **Geographic Filters**
   - Country-specific analysis
   - Regional groupings
   - Custom area selection

2. **Economic Filters**
   - World Bank income classifications
   - GDP-based groupings
   - Development status

3. **Growth Pattern Filters**
   - High growth regions
   - Stable markets
   - Developing areas

4. **Time Period Selection**
   - Year-by-year analysis
   - Custom time ranges
   - Milestone-based periods

## Installation and Setup

```bash
# Clone the repository
git clone https://github.com/jpcurada/global-internet-patterns.git

# Navigate to the project directory
cd global-internet-patterns

# Install required packages
pip install -r requirements.txt

# Run the Streamlit app
streamlit run src/app.py
```

## Project Structure

```
└── global-internet-patterns/
    ├── README.md
    ├── LICENSE
    ├── requirements.txt
    └── src/
        ├── app.py              # Main Streamlit application
        ├── utils.py            # Utility functions
        ├── visuals.py          # Visualization functions
        └── data/              
            ├── internet_gdp_data.csv
            └── processed_data/
```

## About the Author

**John Paul Curada**  
A passionate second-year Computer Science student at the Polytechnic University of the Philippines, exploring the intersection of data science and technology. Committed to using data visualization to tell meaningful stories and drive insights.

- 🎓 Computer Science Student at PUP
- 💡 Interested in Data Science & Visualization
- 🌐 Building impactful data stories

### Connect With Me

- LinkedIn: [Connect with me](https://www.linkedin.com/in/jpcurada/)
- GitHub: [Follow my work](https://github.com/JpCurada)
- DataCamp: [View my competition entry](https://www.datacamp.com/datalab/w/517a04fb-a922-4754-b181-68724be62c47)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Created with 💚 by John Paul Curada