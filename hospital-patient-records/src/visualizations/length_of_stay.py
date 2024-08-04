import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.app.utils import display_aggrid

def plot_length_of_stay_box(data):
    fig = px.box(data, x='ADMISSION_DATE', y='DURATION',
                 title='Distribution of Length of Stay Over Time',
                 labels={'DURATION': 'Length of Stay (hours)', 'ADMISSION_DATE': 'Admission Date'},
                 template='plotly_white')
    fig.update_layout(
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12), tickangle=45),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        title=dict(font=dict(size=18)),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_length_of_stay_heatmap(data):
    data.loc[:, 'AGE_GROUP'] = pd.cut(data['AGE'], bins=[0, 18, 35, 50, 65, 100], labels=['0-18', '19-35', '36-50', '51-65', '66+'])
    pivot_table = data.pivot_table(index='AGE_GROUP', columns='GENDER', values='DURATION', aggfunc='mean').reset_index()

    fig = px.imshow(pivot_table.set_index('AGE_GROUP'),
                    title='Average Length of Stay by Age Group and Gender',
                    labels=dict(x="Gender", y="Age Group", color="Length of Stay (hours)"),
                    color_continuous_scale='YlOrRd',
                    aspect="auto",
                    template='plotly_white')
    fig.update_layout(
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        title=dict(font=dict(size=18)),
        coloraxis_colorbar=dict(title_font=dict(size=14), tickfont=dict(size=12))
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_length_of_stay_trend(data):
    avg_length_of_stay_data = data.groupby('ADMISSION_DATE')['DURATION'].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=avg_length_of_stay_data['ADMISSION_DATE'],
        y=avg_length_of_stay_data['DURATION'],
        mode='lines+markers',
        name='Average Length of Stay',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6, color='#1f77b4', symbol='circle')
    ))
    fig.update_layout(
        title='Average Length of Stay Trend',
        xaxis=dict(title='Admission Date', title_font=dict(size=14), tickfont=dict(size=12), tickangle=45),
        yaxis=dict(title='Average Length of Stay (hours)', title_font=dict(size=14), tickfont=dict(size=12)),
        hovermode='x unified',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

def display_average_length_of_stay(data):
    plot_length_of_stay_trend(data)
    plot_length_of_stay_box(data)
    plot_length_of_stay_heatmap(data)

    with st.expander("View Detailed Length of Stay Data"):
        avg_length_of_stay_data = data.groupby('ADMISSION_DATE')['DURATION'].mean().reset_index()
        display_aggrid(avg_length_of_stay_data.rename(columns={'DURATION': 'Average Length of Stay (hours)'}))

def render_length_of_stay_tab(data):
    st.header("Length of Stay Analysis")
    st.write("This section provides insights into patient length of stay, including trends over time and distribution across different patient groups.")
    display_average_length_of_stay(data)
