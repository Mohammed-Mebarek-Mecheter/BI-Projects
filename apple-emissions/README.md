# Apple's Journey to Carbon Neutrality

This Streamlit dashboard visualizes Apple's progress towards becoming carbon neutral by 2030 using data from their Environmental Progress Reports. It includes interactive visualizations and insights on Apple's emissions, product carbon footprint, and comparison with financial metrics.

## Data

- `data/carbon_footprint_by_product.csv`: Carbon footprint data by product.
- `data/data_dictionary.csv`: Data dictionary describing the fields in the datasets.
- `data/greenhouse_gas_emissions.csv`: Greenhouse gas emissions data.
- `data/normalizing_factors.csv`: Normalizing factors including revenue, market cap, and employees.

## Usage

The dashboard provides the following sections:

### Header Section

- **Title**: "Apple's Journey to Carbon Neutrality"
- **Description**: A brief overview of Apple's pledge to become carbon neutral by 2030.

### Sidebar Filters

- **Year Range Slider**: Filter data by year range.
- **Category Multi-Select Dropdown**: Filter emissions data by category.
- **Type Multi-Select Dropdown**: Filter emissions data by type.
- **Scope Multi-Select Dropdown**: Filter emissions data by scope.

### Key Metrics

- **Baseline Emissions (2015)**
- **Target Emissions (2030)**
- **Current Emissions (2022)**
- **Reduction Percentage**

### Visualizations

1. **Overall Emissions Reduction**: Line chart showing total emissions from 2015 to 2022 with a trend line towards the 2030 target.
    - Insight: Displays the decreasing trend in total emissions.

2. **Emissions by Category, Type, and Scope**: Stacked bar chart showing breakdown of emissions.
    - Insight: Highlights the contribution of product lifecycle emissions and corporate emissions.

3. **Emissions Breakdown Heatmap**: Heatmap showing emissions by category and type over time.
    - Insight: Shows the reduction in emissions across most categories.

4. **Detailed Emissions Data**: Interactive data table using Streamlit AgGrid.

5. **Carbon Footprint by Product**: Scatter plot displaying the carbon footprint of different iPhone models over time.
    - Insight: Shows the trend of decreasing carbon footprint for newer models.

6. **Comparison with Financial Metrics**: Dual-axis line chart comparing emissions trends with revenue and market capitalization trends.
    - Insight: Indicates Apple's success in decoupling financial growth from environmental impact.

### Overall Conclusion

Summarizes the key findings and future steps for Apple to achieve carbon neutrality by 2030.

## References

- [Apple's Environmental Progress Reports](https://www.apple.com/environment/reports/)

## Acknowledgments

This dashboard was created for the Maven Environmental Challenge.
