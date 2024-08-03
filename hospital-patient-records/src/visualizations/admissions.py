import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.app.utils import display_aggrid

def plot_admissions_area(data):
    fig = px.area(data, x='ADMISSION_DATE', y='count',
                  title='Cumulative Admissions Over Time',
                  labels={'count': 'Number of Admissions', 'ADMISSION_DATE': 'Date'},
                  line_shape='spline',
                  template='plotly_white')
    fig.update_traces(fill='tozeroy', line=dict(color='#1f77b4'))
    fig.update_layout(
        hovermode='x unified',
        hoverlabel=dict(bgcolor="white", font_size=12),
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        title=dict(font=dict(size=18))
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_admissions_line_markers(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['ADMISSION_DATE'],
        y=data['count'],
        mode='lines+markers',
        name='Admissions',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6, color='#1f77b4', symbol='circle')
    ))
    fig.update_layout(
        title='Admissions Over Time with Markers',
        xaxis_title='Date',
        yaxis_title='Number of Admissions',
        template='plotly_white',
        hovermode='x unified',
        hoverlabel=dict(bgcolor="white", font_size=12),
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
    )
    st.plotly_chart(fig, use_container_width=True)

def display_admissions(data):
    admissions_data = data.groupby('ADMISSION_DATE').size().reset_index(name='count')
    admissions_data = admissions_data.sort_values('ADMISSION_DATE')

    plot_admissions_area(admissions_data)
    plot_admissions_line_markers(admissions_data)

    with st.expander("View Detailed Admissions Data"):
        display_aggrid(admissions_data.rename(columns={'count': 'Number of Admissions'}))

def render_admissions_tab(data):
    st.header("Admissions Over Time")
    st.write("This section provides insights into the hospital's admission trends over time.")
    display_admissions(data)