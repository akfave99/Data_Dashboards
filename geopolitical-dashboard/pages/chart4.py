"""
Chart 4 Page - Multi-Country Influence Radar Chart
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from chart_data import get_data, filter_data

dash.register_page(__name__, path='/chart4', name='Multi-Country Radar')

component_id = "multi_country_influence_radar"
country_selector_id = f"{component_id}_countries"
metric_selector_id = f"{component_id}_metric"

def create_radar_figure(selected_countries=None, metric_type="influence"):
    """Create radar chart for selected countries."""
    df = filter_data(get_data())

    if selected_countries is None:
        selected_countries = df['Country'].unique().tolist()

    if not selected_countries or len(df) == 0:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No data available",
            annotations=[{
                "text": "Please select at least one country to display",
                "showarrow": False,
                "font": {"size": 20}
            }]
        )
        return empty_fig

    # Define the metrics based on selection
    if metric_type == "influence":
        metric_columns = ['Influence_US_numeric', 'Influence_Russia_numeric', 'Influence_China_numeric', 'Influence_Turkiye_Israel_numeric']
        metric_labels = ['US Influence', 'Russia Influence', 'China Influence', 'Türkiye/Israel Influence']
    else:  # matrix
        metric_columns = ['Matrix_US_numeric', 'Matrix_Russia_numeric', 'Matrix_China_numeric', 'Matrix_Turkiye_Israel_numeric']
        metric_labels = ['US Matrix', 'Russia Matrix', 'China Matrix', 'Türkiye/Israel Matrix']

    # Create radar chart
    fig = go.Figure()

    # Add a trace for each selected country
    for country in selected_countries:
        country_data = df[df['Country'] == country]
        if len(country_data) == 0:
            continue

        row = country_data.iloc[0]

        # Extract values for radar chart, handling NaN values
        values = []
        for col in metric_columns:
            val = row.get(col, np.nan)
            if pd.isna(val):
                val = 0
            values.append(float(val))

        # Close the radar chart by repeating the first value
        values_closed = values + [values[0]]
        labels_closed = metric_labels + [metric_labels[0]]

        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill='toself',
            name=country,
            line=dict(width=2),
            opacity=0.7
        ))

    # Update layout for radar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3],
                tickvals=[1, 2, 3],
                ticktext=['Low', 'Medium', 'High']
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.05
        ),
        title="Multi-Country Influence Radar Chart",
        height=700
    )
    return fig

# Get unique countries for dropdown
df_data = get_data()
unique_countries = df_data['Country'].unique().tolist()
country_options = [{'label': country, 'value': country} for country in unique_countries]
default_countries = unique_countries

layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.Div([
                html.H1("Multi-Country Influence Radar Comparison", className="page-title"),
                html.P("Radar chart for comparing influence metrics across multiple countries simultaneously. Each country appears as a separate colored trace, with suppliers (US, Russia, China, Türkiye/Israel) positioned around the perimeter. Select multiple countries to overlay and compare their influence patterns. Toggle between Influence and Matrix metrics to analyze different aspects of supplier relationships.", className="page-subtitle"),
            ]), width=12),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                html.Label("Select Countries:", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id=country_selector_id,
                    options=country_options,
                    value=default_countries,
                    multi=True,
                    style={"minWidth": "300px"}
                ),
            ], width=6),
            dbc.Col([
                html.Label("Select Metric Type:", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id=metric_selector_id,
                    options=[
                        {"label": "Influence Metrics", "value": "influence"},
                        {"label": "Matrix Metrics", "value": "matrix"}
                    ],
                    value="influence",
                    style={"minWidth": "200px"}
                ),
            ], width=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='chart4-graph', style={'height': '80vh'}, config={'responsive': True}), width=12),
        ], className="mb-4"),
    ],
    fluid=True,
    className="page-content"
)

@callback(
    Output('chart4-graph', 'figure'),
    [Input(country_selector_id, 'value'), Input(metric_selector_id, 'value')]
)
def update_chart(selected_countries, metric_type):
    return create_radar_figure(selected_countries or default_countries, metric_type or "influence")
