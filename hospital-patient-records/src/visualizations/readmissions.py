import streamlit as st
import plotly.graph_objects as go
from src.app.utils import display_aggrid

def plot_dual_axis_line(admissions_data, readmissions_data):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=admissions_data['ADMISSION_DATE'],
        y=admissions_data['count'],
        mode='lines',
        name='Admissions',
        line=dict(color='#1f77b4', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=readmissions_data['ADMISSION_DATE'],
        y=readmissions_data['count'],
        mode='lines',
        name='Readmissions',
        line=dict(color='#ff7f0e', width=2),
        yaxis='y2'
    ))

    fig.update_layout(
        title='Admissions and Readmissions Over Time',
        xaxis=dict(title='Date', title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(
            title='Number of Admissions',
            titlefont=dict(color='#1f77b4', size=14),
            tickfont=dict(color='#1f77b4', size=12),
            side='left'
        ),
        yaxis2=dict(
            title='Number of Readmissions',
            titlefont=dict(color='#ff7f0e', size=14),
            tickfont=dict(color='#ff7f0e', size=12),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.8)'),
        hovermode='x unified',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_sankey_diagram(data):
    nodes = ["Admitted", "Discharged", "Readmitted"]
    counts = data.groupby(['ENCOUNTERCLASS', 'READMISSION']).size().reset_index(name='count')

    admitted = counts[counts['READMISSION'] == 0]['count'].sum()
    discharged = admitted
    readmitted = counts[counts['READMISSION'] == 1]['count'].sum()

    source = [0, 1, 1]
    target = [1, 2, 1]
    value = [admitted, readmitted, discharged - readmitted]

    node_colors = ['#1f77b4', '#2ca02c', '#ff7f0e']

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=['rgba(31, 119, 180, 0.4)', 'rgba(255, 127, 14, 0.4)', 'rgba(44, 160, 44, 0.4)']
        )
    ))

    fig.update_layout(
        title_text="Patient Flow and Transitions",
        font_size=12,
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

def display_readmissions(data):
    readmissions_data = data[data['READMISSION'] == 1].groupby('ADMISSION_DATE').size().reset_index(name='count')
    admissions_data = data.groupby('ADMISSION_DATE').size().reset_index(name='count')

    readmissions_data = readmissions_data.sort_values('ADMISSION_DATE')
    admissions_data = admissions_data.sort_values('ADMISSION_DATE')

    plot_dual_axis_line(admissions_data, readmissions_data)
    plot_sankey_diagram(data)

    with st.expander("View Detailed Readmissions Data"):
        display_aggrid(readmissions_data.rename(columns={'count': 'Number of Readmissions'}))

def render_readmissions_tab(data):
    st.header("Readmissions Analysis")
    st.write("This section provides insights into the hospital's readmission patterns and their relationship with overall admissions.")
    display_readmissions(data)