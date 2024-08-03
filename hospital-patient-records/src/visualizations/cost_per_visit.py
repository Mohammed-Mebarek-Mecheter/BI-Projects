import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.app.utils import display_aggrid

def plot_cost_per_visit_trend(data):
    avg_cost_per_visit_data = data.groupby('ADMISSION_DATE')['TOTAL_CLAIM_COST'].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=avg_cost_per_visit_data['ADMISSION_DATE'],
        y=avg_cost_per_visit_data['TOTAL_CLAIM_COST'],
        mode='lines+markers',
        name='Average Cost Per Visit',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6, color='#1f77b4', symbol='circle')
    ))
    fig.update_layout(
        title='Average Cost Per Visit Trend',
        xaxis=dict(title='Admission Date', title_font=dict(size=14), tickfont=dict(size=12), tickangle=45),
        yaxis=dict(title='Average Cost Per Visit ($)', title_font=dict(size=14), tickfont=dict(size=12)),
        hovermode='x unified',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_cost_per_visit_scatter(data):
    fig = px.scatter(data, x='DURATION', y='TOTAL_CLAIM_COST',
                     title='Cost Per Visit vs. Length of Stay',
                     labels={'DURATION': 'Length of Stay (hours)', 'TOTAL_CLAIM_COST': 'Cost Per Visit ($)'},
                     template='plotly_white',
                     color='AGE_GROUP',
                     hover_data=['GENDER', 'AGE'])
    fig.update_layout(
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        legend=dict(title='Age Group', font=dict(size=12)),
        title=dict(font=dict(size=18))
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_cost_per_visit_treemap(data):
    data['AGE_GROUP'] = pd.cut(data['AGE'], bins=[0, 18, 35, 50, 65, 100], labels=['0-18', '19-35', '36-50', '51-65', '66+'])
    fig = px.treemap(data, path=['AGE_GROUP', 'GENDER'], values='TOTAL_CLAIM_COST', title='Distribution of Costs Among Different Categories (Treemap)')
    st.plotly_chart(fig, use_container_width=True)


def display_average_cost_per_visit(data):
    plot_cost_per_visit_trend(data)
    plot_cost_per_visit_scatter(data)
    plot_cost_per_visit_treemap(data)

    with st.expander("View Detailed Cost Per Visit Data"):
        avg_cost_per_visit_data = data.groupby('ADMISSION_DATE')['TOTAL_CLAIM_COST'].mean().reset_index()
        display_aggrid(avg_cost_per_visit_data.rename(columns={'TOTAL_CLAIM_COST': 'Average Cost Per Visit ($)'}))

def render_cost_per_visit_tab(data):
    st.header("Cost Per Visit Analysis")
    st.write("This section provides insights into the costs associated with patient visits, including trends over time and relationships with other factors.")
    data['AGE_GROUP'] = pd.cut(data['AGE'], bins=[0, 18, 35, 50, 65, 100], labels=['0-18', '19-35', '36-50', '51-65', '66+'])
    display_average_cost_per_visit(data)
