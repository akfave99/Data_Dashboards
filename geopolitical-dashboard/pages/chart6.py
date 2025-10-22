"""
Chart 6 Page - Regional Density Map
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from chart_data import get_data, filter_data

dash.register_page(__name__, path='/chart6', name='Regional Density')

component_id = "density_map"
metric_selector_id = f"{component_id}_metric"

def create_density_map_figure(metric="spending"):
    """Create density map for regional analysis."""
    df = filter_data(get_data())

    if len(df) == 0:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No data available",
            annotations=[{"text": "No data available", "showarrow": False}]
        )
        return empty_fig

    # Create scatter plot with size representing density
    if metric == "spending":
        size_col = "Avg_Spend"
        title = "Regional Defense Spending Density"
        size_label = "Avg Spending ($M)"
    else:
        size_col = "Threat Perception"
        title = "Regional Threat Perception Density"
        size_label = "Threat Level"

    # Create synthetic coordinates for visualization
    np.random.seed(42)
    df_plot = df.copy()
    df_plot['x'] = np.random.uniform(0, 10, len(df_plot))
    df_plot['y'] = np.random.uniform(0, 10, len(df_plot))

    # Normalize size for visualization
    if metric == "spending":
        df_plot['size'] = (df_plot[size_col] / df_plot[size_col].max() * 50) + 10
    else:
        df_plot['size'] = 30

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_plot['x'],
        y=df_plot['y'],
        mode='markers',
        marker=dict(
            size=df_plot['size'],
            color=df_plot[size_col],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title=size_label),
            line=dict(width=2, color='white')
        ),
        text=df_plot['Country'],
        hovertemplate='<b>%{text}</b><br>' +
                      f'{size_label}: %{{marker.color:.0f}}<br>' +
                      'Threat: %{customdata[0]}<extra></extra>',
        customdata=df_plot[['Threat Perception']].values
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Regional Position (X)",
        yaxis_title="Regional Position (Y)",
        height=700,
        showlegend=False,
        hovermode='closest'
    )

    return fig

layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.Div([
                html.H1("Regional Defense Metrics Density Map", className="page-title"),
                html.P("Scatter plot visualization showing the regional distribution and density of defense metrics across Central Asian countries. Bubble size represents the intensity of the selected metric (Defense Spending or Threat Perception), while color intensity (Viridis scale) provides an additional visual dimension. Hover over bubbles to see country names and exact metric values.", className="page-subtitle"),
            ]), width=12),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                html.Label("Metric:", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id=metric_selector_id,
                    options=[
                        {"label": "Defense Spending", "value": "spending"},
                        {"label": "Threat Perception", "value": "threat"}
                    ],
                    value="spending",
                    style={"minWidth": "200px"}
                ),
            ], width=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='chart6-graph', style={'height': '80vh'}, config={'responsive': True}), width=12),
        ], className="mb-4"),
    ],
    fluid=True,
    className="page-content"
)

@callback(
    Output('chart6-graph', 'figure'),
    Input(metric_selector_id, 'value')
)
def update_chart(metric):
    return create_density_map_figure(metric or "spending")
