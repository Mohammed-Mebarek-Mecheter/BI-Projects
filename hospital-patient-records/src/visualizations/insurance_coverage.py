import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.app.utils import display_aggrid

def plot_insurance_coverage_trend(data):
    insurance_coverage_data = data.groupby('ADMISSION_DATE')['COVERED_BY_INSURANCE'].mean().reset_index()
    insurance_coverage_data['COVERED_BY_INSURANCE'] *= 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=insurance_coverage_data['ADMISSION_DATE'],
        y=insurance_coverage_data['COVERED_BY_INSURANCE'],
        mode='lines+markers',
        name='Insurance Coverage',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6, color='#1f77b4', symbol='circle')
    ))
    fig.update_layout(
        title='Insurance Coverage Trend',
        xaxis=dict(title='Admission Date', title_font=dict(size=14), tickfont=dict(size=12), tickangle=45),
        yaxis=dict(title='Percentage Covered by Insurance (%)', title_font=dict(size=14), tickfont=dict(size=12)),
        hovermode='x unified',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_insurance_coverage_stacked_bar(data):
    data['AGE_GROUP'] = pd.cut(data['AGE'], bins=[0, 18, 35, 50, 65, 100], labels=['0-18', '19-35', '36-50', '51-65', '66+'])
    coverage_by_age_gender = data.groupby(['AGE_GROUP', 'GENDER'])['COVERED_BY_INSURANCE'].mean().reset_index()
    coverage_by_age_gender['COVERED_BY_INSURANCE'] *= 100

    fig = px.bar(coverage_by_age_gender, x='AGE_GROUP', y='COVERED_BY_INSURANCE', color='GENDER',
                 title='Insurance Coverage by Age Group and Gender',
                 labels={'COVERED_BY_INSURANCE': 'Percentage Covered (%)', 'AGE_GROUP': 'Age Group'},
                 template='plotly_white',
                 color_discrete_sequence=['#1f77b4', '#ff7f0e'])

    fig.update_layout(
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        legend=dict(title='Gender', font=dict(size=12)),
        title=dict(font=dict(size=18)),
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_insurance_coverage_bubble_chart(data):
    coverage_and_costs = data.groupby('PAYER').agg({'COVERED_BY_INSURANCE': 'mean', 'TOTAL_CLAIM_COST': 'sum'}).reset_index()
    fig = px.scatter(coverage_and_costs, x='COVERED_BY_INSURANCE', y='TOTAL_CLAIM_COST', size='TOTAL_CLAIM_COST', color='PAYER',
                     title='Percentage of Procedures Covered by Insurance and Their Respective Costs (Bubble Chart)',
                     labels={'COVERED_BY_INSURANCE': 'Percentage Covered by Insurance (%)', 'TOTAL_CLAIM_COST': 'Total Claim Cost ($)'})
    st.plotly_chart(fig, use_container_width=True)


def display_insurance_coverage(data):
    try:
        plot_insurance_coverage_trend(data)
        plot_insurance_coverage_stacked_bar(data)
        plot_insurance_coverage_bubble_chart(data)

        with st.expander("View Detailed Insurance Coverage Data"):
            insurance_coverage_data = data.groupby('ADMISSION_DATE')['COVERED_BY_INSURANCE'].mean().reset_index()
            insurance_coverage_data['COVERED_BY_INSURANCE'] *= 100
            display_aggrid(insurance_coverage_data.rename(columns={'COVERED_BY_INSURANCE': 'Percentage Covered by Insurance (%)'}))
    except Exception as e:
        st.error(f"An error occurred while displaying insurance coverage data: {str(e)}")

def render_insurance_coverage_tab(data):
    st.header("Insurance Coverage Analysis")
    st.write("This section provides insights into insurance coverage trends, patterns across different patient groups, and relationships with costs.")
    display_insurance_coverage(data)