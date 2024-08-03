import streamlit as st
from src.app.utils import load_data, filter_data_by_criteria
from src.app.components import render_sidebar
from src.visualizations.admissions import render_admissions_tab
from src.visualizations.readmissions import render_readmissions_tab
from src.visualizations.length_of_stay import render_length_of_stay_tab
from src.visualizations.cost_per_visit import render_cost_per_visit_tab
from src.visualizations.insurance_coverage import render_insurance_coverage_tab

# Load data
data = load_data()

# Set page configuration
st.set_page_config(layout="wide")

# Title and Summary
st.title("Massachusetts General Hospital KPI Dashboard")
st.markdown("""
This dashboard provides insights into Massachusetts General Hospital's performance metrics over recent years. 
You can explore admissions, readmissions, average length of stay, average cost per visit, and insurance coverage through interactive visualizations and tables.
""")

# Sidebar for filters
start_date, end_date, age_group, gender, encounter_class, insurance_provider, readmitted = render_sidebar(data)

# Filter data based on selected criteria
filtered_data = filter_data_by_criteria(data, start_date, end_date, age_group, gender, encounter_class, insurance_provider, readmitted)

# Tabs for different metrics
tabs = st.tabs(["Admissions Over Time", "Readmissions Over Time", "Average Length of Stay", "Average Cost Per Visit", "Insurance Coverage"])

# Tab content
with tabs[0]:
    render_admissions_tab(filtered_data)

with tabs[1]:
    render_readmissions_tab(filtered_data)

with tabs[2]:
    render_length_of_stay_tab(filtered_data)

with tabs[3]:
    render_cost_per_visit_tab(filtered_data)

with tabs[4]:
    render_insurance_coverage_tab(filtered_data)

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
        <p>Data source: <a href="https://mavenanalytics.io/">Maven Analytics</a> | Last updated: August 02, 2024</p>
    </div>
    """, unsafe_allow_html=True
)
