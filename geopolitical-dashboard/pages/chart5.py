"""
Chart 5 Page - Defense Priorities Correlation Heatmap
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

dash.register_page(__name__, path='/chart5', name='Priorities Heatmap')

component_id = "defense_priorities_correlation_heatmap"
grouping_control_id = f"{component_id}_grouping"
intensity_control_id = f"{component_id}_intensity"

def create_heatmap_figure(grouping="country", intensity_metric="influence"):
    """Create correlation heatmap for defense priorities."""
    df = filter_data(get_data())

    if len(df) == 0:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No data available",
            annotations=[{"text": "No data available", "showarrow": False}]
        )
        return empty_fig

    # Define metrics based on intensity selection
    if intensity_metric == "influence":
        metric_cols = ['Influence_US_numeric', 'Influence_Russia_numeric', 'Influence_China_numeric', 'Influence_Turkiye_Israel_numeric']
        metric_labels = ['US', 'Russia', 'China', 'Türkiye/Israel']
    else:
        metric_cols = ['Matrix_US_numeric', 'Matrix_Russia_numeric', 'Matrix_China_numeric', 'Matrix_Turkiye_Israel_numeric']
        metric_labels = ['US', 'Russia', 'China', 'Türkiye/Israel']

    # Create correlation matrix
    if grouping == "country":
        countries = df['Country'].unique()
        z_data = []
        for country in countries:
            country_data = df[df['Country'] == country]
            row = []
            for col in metric_cols:
                val = country_data[col].iloc[0] if len(country_data) > 0 else 0
                row.append(float(val) if pd.notna(val) else 0)
            z_data.append(row)

        fig = go.Figure(data=go.Heatmap(
            z=z_data,
            x=metric_labels,
            y=countries,
            colorscale='RdYlBu_r',
            colorbar=dict(title="Influence Level")
        ))
        fig.update_layout(
            title="Defense Priorities by Country and Supplier",
            xaxis_title="Supplier",
            yaxis_title="Country",
            height=600
        )
    else:  # supplier
        suppliers = metric_labels
        z_data = []
        for i, supplier in enumerate(suppliers):
            row = []
            for country in df['Country'].unique():
                country_data = df[df['Country'] == country]
                val = country_data[metric_cols[i]].iloc[0] if len(country_data) > 0 else 0
                row.append(float(val) if pd.notna(val) else 0)
            z_data.append(row)

        fig = go.Figure(data=go.Heatmap(
            z=z_data,
            x=df['Country'].unique(),
            y=suppliers,
            colorscale='RdYlBu_r',
            colorbar=dict(title="Influence Level")
        ))
        fig.update_layout(
            title="Defense Priorities by Supplier and Country",
            xaxis_title="Country",
            yaxis_title="Supplier",
            height=600
        )

    return fig

layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.Div([
                html.H1("Defense Priorities Correlation Heatmap", className="page-title"),
                html.P("Heatmap visualization showing the correlation between defense priorities and suppliers. Choose to view data grouped by Country (countries on Y-axis, suppliers on X-axis) or by Supplier (suppliers on Y-axis, countries on X-axis). Color intensity represents the strength of the relationship, with red indicating high values and blue indicating low values. Toggle between Influence and Matrix metrics for different analytical perspectives.", className="page-subtitle"),
            ]), width=12),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                html.Label("Grouping:", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id=grouping_control_id,
                    options=[
                        {"label": "By Country", "value": "country"},
                        {"label": "By Supplier", "value": "supplier"}
                    ],
                    value="country",
                    style={"minWidth": "200px"}
                ),
            ], width=6),
            dbc.Col([
                html.Label("Intensity Metric:", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id=intensity_control_id,
                    options=[
                        {"label": "Influence", "value": "influence"},
                        {"label": "Matrix", "value": "matrix"}
                    ],
                    value="influence",
                    style={"minWidth": "200px"}
                ),
            ], width=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='chart5-graph', style={'height': '80vh'}, config={'responsive': True}), width=12),
        ], className="mb-4"),
    ],
    fluid=True,
    className="page-content"
)

@callback(
    Output('chart5-graph', 'figure'),
    [Input(grouping_control_id, 'value'), Input(intensity_control_id, 'value')]
)
def update_chart(grouping, intensity_metric):
    return create_heatmap_figure(grouping or "country", intensity_metric or "influence")
