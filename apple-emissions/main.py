import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Set the page configuration
st.set_page_config(page_title="Apple's Journey to Carbon Neutrality", layout="wide")

# Load the datasets
@st.cache_data
def load_data():
    carbon = pd.read_csv('data/carbon_footprint_by_product.csv')
    greenhouse = pd.read_csv('data/greenhouse_gas_emissions.csv')
    factors = pd.read_csv('data/normalizing_factors.csv')
    return carbon, greenhouse, factors

carbon, greenhouse, factors = load_data()

# Clean the data
greenhouse['Fiscal Year'] = pd.to_datetime(greenhouse['Fiscal Year'], format='%Y')
carbon['Release Year'] = pd.to_datetime(carbon['Release Year'], format='%Y')
factors['Fiscal Year'] = pd.to_datetime(factors['Fiscal Year'], format='%Y')

# Fill missing Scope values related to "Carbon removals" with "Unknown"
greenhouse.loc[greenhouse['Scope'].isnull() & (greenhouse['Type'] == 'Carbon removals'), 'Scope'] = 'Unknown'

# Fill missing Emissions values with median
greenhouse['Emissions'].fillna(greenhouse['Emissions'].median(), inplace=True)

# Header Section
st.title("Apple's Journey to Carbon Neutrality")
st.write("This dashboard visualizes Apple's progress towards becoming carbon neutral by 2030 using data from their Environmental Progress Reports.")

# Sidebar for filters
st.sidebar.header("Filters")
year_range = st.sidebar.slider("Select Year Range", min_value=2015, max_value=2022, value=(2015, 2022))
categories = st.sidebar.multiselect("Select Categories", options=greenhouse['Category'].unique(), default=greenhouse['Category'].unique())
types = st.sidebar.multiselect("Select Types", options=greenhouse['Type'].unique(), default=greenhouse['Type'].unique())
scopes = st.sidebar.multiselect("Select Scopes", options=greenhouse['Scope'].unique(), default=greenhouse['Scope'].unique())

# Filter data based on sidebar selections
filtered_greenhouse = greenhouse[
    (greenhouse['Fiscal Year'].dt.year.between(year_range[0], year_range[1])) &
    (greenhouse['Category'].isin(categories)) &
    (greenhouse['Type'].isin(types)) &
    (greenhouse['Scope'].isin(scopes))
    ]

# Key Metrics/KPIs
baseline_emissions = 38.4  # million metric tons CO2e
target_emissions = 9.6  # million metric tons CO2e
current_emissions = filtered_greenhouse[filtered_greenhouse['Fiscal Year'].dt.year == 2022]['Emissions'].sum() / 1e6  # Convert to million metric tons
reduction_percentage = ((baseline_emissions - current_emissions) / baseline_emissions) * 100

st.header("Key Metrics")

# Create a card-like layout for metrics
def metric_card(title, value, key):
    st.markdown(f"""
    <div style="
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
        <h3>{title}</h3>
        <h2>{value}</h2>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    metric_card("Baseline Emissions (2015)", f"{baseline_emissions:.2f} Mt CO2e", "baseline")
with col2:
    metric_card("Target Emissions (2030)", f"{target_emissions:.2f} Mt CO2e", "target")

col3, col4 = st.columns(2)
with col3:
    metric_card("Current Emissions (2022)", f"{current_emissions:.2f} Mt CO2e", "current")
with col4:
    metric_card("Reduction Percentage", f"{reduction_percentage:.2f}%", "reduction")

# Overall Emissions Reduction
st.header("Overall Emissions Reduction")
emissions_over_time = filtered_greenhouse.groupby(filtered_greenhouse['Fiscal Year'].dt.year)['Emissions'].sum().reset_index()
emissions_over_time.columns = ['Year', 'Total Emissions']
emissions_over_time['Target'] = emissions_over_time.apply(lambda x: target_emissions if x['Year'] >= 2023 else None, axis=1)

fig = go.Figure()
fig.add_trace(go.Scatter(x=emissions_over_time['Year'], y=emissions_over_time['Total Emissions'],
                         mode='lines+markers', name='Actual Emissions'))
fig.add_trace(go.Scatter(x=emissions_over_time['Year'], y=emissions_over_time['Target'],
                         mode='lines', name='2030 Target', line=dict(dash='dash')))
fig.update_layout(title="Total Emissions from 2015 to 2022 with 2030 Target",
                  xaxis_title="Year", yaxis_title="Emissions (metric tons CO2e)")
st.plotly_chart(fig, use_container_width=True)

# Add insight
st.write("""
From 2015 to 2022, there is a clear trend of decreasing total emissions. This indicates that Apple is making consistent progress towards its goal of reducing emissions to 9.6 million metric tons CO2e by 2030.
""")

# Emissions by Category, Type, and Scope
st.header("Emissions by Category, Type, and Scope")

# Prepare data for stacked bar chart
emissions_breakdown = filtered_greenhouse.groupby(['Fiscal Year', 'Category', 'Type', 'Scope'])['Emissions'].sum().reset_index()

# Create stacked bar chart
fig = px.bar(emissions_breakdown, x='Fiscal Year', y='Emissions',
             color='Category', pattern_shape='Type', pattern_shape_sequence=[".", "x", "+"],
             hover_data=['Scope'],
             title="Emissions Breakdown by Category, Type, and Scope",
             labels={'Emissions': 'Emissions (metric tons CO2e)'})

fig.update_layout(barmode='stack', xaxis_title="Fiscal Year")
st.plotly_chart(fig, use_container_width=True)

# Add insight
st.write("""
This stacked bar chart shows the breakdown of emissions by category, type, and scope. It highlights that product lifecycle emissions are a significant contributor to overall emissions. Corporate emissions, though lower, still play a crucial role.
""")

# Emissions Breakdown Heatmap
st.header("Emissions Breakdown")

# Prepare data for heatmap
heatmap_data = filtered_greenhouse.pivot_table(
    values='Emissions',
    index=['Category', 'Type'],
    columns='Fiscal Year',
    aggfunc='sum'
)

# Create heatmap using seaborn
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax)
plt.title('Emissions Breakdown by Category and Type Over Time')
plt.ylabel('Category - Type')
plt.xlabel('Fiscal Year')
st.pyplot(fig)

# Add insight
st.write("""
This heatmap reveals the changes in emissions by category and type over the years. The darker colors represent higher emissions. A notable observation is the consistent reduction in emissions across most categories, showcasing Apple's efforts in lowering its carbon footprint.
""")

# Interactive data table using streamlit-aggrid
st.subheader("Detailed Emissions Data")

gb = GridOptionsBuilder.from_dataframe(emissions_breakdown)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_side_bar()
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children")
gridOptions = gb.build()

grid_response = AgGrid(
    emissions_breakdown,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    fit_columns_on_grid_load=False,
    theme='streamlit', # Add theme color to the table
    enable_enterprise_modules=True,
    height=350,
    width='100%',
    reload_data=True
)

# Carbon Footprint by Product
st.header("Carbon Footprint by Product")
carbon['Year'] = carbon['Release Year'].dt.year
carbon['Size'] = carbon['Carbon Footprint'] / 1000  # Adjust size for better visualization

fig = px.scatter(carbon, x='Year', y='Carbon Footprint', size='Size', color='Product',
                 hover_name='Product', text='Product',
                 title="Carbon Footprint by Product Over Time")
fig.update_traces(textposition='top center')
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Add insight
st.write("""
This scatter plot shows the carbon footprint of different iPhone models over time. The size of the bubbles represents the carbon footprint, with larger bubbles indicating higher emissions. There is a visible trend of decreasing carbon footprint for newer models, reflecting Apple's improvements in product design and manufacturing processes.
""")

# Comparison with Financial Metrics
st.header("Comparison with Financial Metrics")
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x=factors['Fiscal Year'], y=factors['Revenue'],
                         mode='lines', name='Revenue'), secondary_y=False)
fig.add_trace(go.Scatter(x=factors['Fiscal Year'], y=factors['Market Capitalization'],
                         mode='lines', name='Market Cap'), secondary_y=False)
fig.add_trace(go.Scatter(x=emissions_over_time['Year'], y=emissions_over_time['Total Emissions'],
                         mode='lines', name='Emissions'), secondary_y=True)

fig.update_layout(title="Comparison of Emissions with Revenue and Market Cap",
                  xaxis_title="Year")
fig.update_yaxes(title_text="USD (Billions)", secondary_y=False)
fig.update_yaxes(title_text="Emissions (metric tons CO2e)", secondary_y=True)

st.plotly_chart(fig, use_container_width=True)

# Add insight
st.write("""
This dual-axis line chart compares Apple's emissions with its revenue and market capitalization from 2015 to 2022. Despite significant growth in revenue, Apple has managed to reduce its overall emissions. This indicates that the company is successfully decoupling its financial growth from its environmental impact.
""")

# Overall Conclusion
st.header("Overall Conclusion")
st.write(f"""
To fully achieve carbon neutrality by 2030, Apple will need to:
- Continue improving energy efficiency across its operations and supply chain.
- Increase its use of renewable energy.
- Invest in carbon removal projects to offset the remaining emissions.
- Further innovate in product design to reduce the carbon footprint of its devices.
""")

# Footer
st.write("### References")
st.write("[Apple's Environmental Progress Reports](https://www.apple.com/environment/reports/)")
st.write("[Dashboard created for the Maven Environmental Challenge](https://mavenanalytics.io/challenges/maven-environmental-challenge/ec3b9855-923d-4647-ac7a-c6ded422b2b7)")

# Footer
st.markdown(
    """
    <div style='text-align: center;'>
        <h3>Made with ❤️ by Mebarek</h3>
        <p>Connect with me:</p>
    </div>
    """, unsafe_allow_html=True
)

# Display social media links side by side and centered
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("<div style='text-align: center;'><a href='https://github.com/Mohammed-Mebarek-Mecheter/' target='_blank'>GitHub</a></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='text-align: center;'><a href='https://www.linkedin.com/in/mohammed-mecheter/' target='_blank'>LinkedIn</a></div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div style='text-align: center;'><a href='https://mebarek.pages.dev/' target='_blank'>Portfolio</a></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div style='text-align: center;'>
        <p>Data source: <a href="https://mavenanalytics.io/">Maven Analytics</a> | Last updated: August 04, 2024</p>
    </div>
    """, unsafe_allow_html=True
)
