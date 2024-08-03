import streamlit as st
from datetime import datetime

def render_sidebar(data):
    st.sidebar.title("Filters")

    start_date = st.sidebar.date_input('Start date', datetime.strptime("2022-01-01", "%Y-%m-%d"))
    end_date = st.sidebar.date_input('End date', datetime.strptime("2022-12-31", "%Y-%m-%d"))

    age_group = st.sidebar.selectbox('Age Group', ['All', '0-18', '19-35', '36-50', '51-65', '66+'])
    gender = st.sidebar.selectbox('Gender', ['All', 'Male', 'Female', 'Other'])
    encounter_class = st.sidebar.selectbox('Encounter Class', ['All', 'Inpatient', 'Outpatient', 'Emergency', 'Ambulatory'])
    insurance_provider = st.sidebar.selectbox('Insurance Provider', ['All'] + list(data['PAYER'].unique()))
    readmitted = st.sidebar.selectbox('Readmitted', ['All', 'Yes', 'No'])

    return start_date, end_date, age_group, gender, encounter_class, insurance_provider, readmitted
