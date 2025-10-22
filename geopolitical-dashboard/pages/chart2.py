"""
Chart 2 Page - Regional Threat Perception and Defense Influence
"""

import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os

dash.register_page(__name__, path='/chart2', name='Regional Influence Map')

# Import data module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chart_data import get_data, filter_data

# Component configuration
component_id = "threat_perception_choropleth_map"
control_id = f"{component_id}_color_by"

control_options = [
    {"label": "US Influence", "value": "Influence_US_numeric"},
    {"label": "Russia Influence", "value": "Influence_Russia_numeric"},
    {"label": "China Influence", "value": "Influence_China_numeric"},
    {"label": "Turkey/Israel Influence", "value": "Influence_Turkiye_Israel_numeric"}
]
control_default = "Influence_US_numeric"


def create_choropleth_figure(color_by=control_default):
    """Create the choropleth map."""
    df = filter_data(get_data()).copy()

    if len(df) == 0:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No data available",
            annotations=[{
                "text": "No data is available to display",
                "showarrow": False,
                "font": {"size": 20}
            }]
        )
        return empty_fig

    # Create ISO-3 country codes mapping for choropleth
    country_iso_mapping = {
        'Kazakhstan': 'KAZ',
        'Turkmenistan': 'TKM',
        'Azerbaijan': 'AZE',
        'Georgia': 'GEO',
        'Uzbekistan': 'UZB'
    }

    df['iso_alpha'] = df['Country'].map(country_iso_mapping)

    # Handle missing values in the color column
    df[color_by] = pd.to_numeric(df[color_by], errors='coerce')

    # Create custom hover text with threat perception and defense priorities
    df['hover_text'] = df.apply(lambda row:
        f"<b>{row['Country']}</b><br>" +
        f"Threat Perception: {row['Threat Perception']}<br>" +
        f"Defense Priorities: {row['Defense Priorities']}<br>" +
        f"Key Suppliers: {row['Suppliers']}<br>" +
        f"Influence Level: {row[color_by] if pd.notna(row[color_by]) else 'N/A'}",
        axis=1
    )

    # Get the influence type for the title
    influence_type = color_by.replace('Influence_', '').replace('_numeric', '').replace('_', '/')

    # Create choropleth map
    fig = px.choropleth(
        df,
        locations='iso_alpha',
        color=color_by,
        hover_name='Country',
        custom_data=['hover_text'],
        color_continuous_scale='RdYlBu_r',
        range_color=[1, 3] if df[color_by].notna().any() else [0, 1],
        labels={color_by: f'{influence_type} Influence Level'}
    )

    # Update hover template to show custom text
    fig.update_traces(
        hovertemplate='%{customdata[0]}<extra></extra>'
    )

    # Update layout for better visualization
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth',
            center=dict(lat=42, lon=55),  # Center on Central Asia/Caucasus region
            projection_scale=3
        ),
        coloraxis_colorbar=dict(
            title=f"{influence_type} Influence",
            tickvals=[1, 2, 3],
            ticktext=['Low', 'Medium', 'High']
        ),
        height=700
    )

    return fig


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H1("Regional Supplier Influence Choropleth Map", className="page-title"),
                            html.P("Geographic visualization of Central Asia and the Caucasus region with countries color-coded by defense supplier influence levels. Select different suppliers to see how their influence varies across the region. Color intensity represents influence strength from Low (1) to High (3).", className="page-subtitle"),
                        ]
                    ),
                    width=12
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Label("Color by Influence:", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id=control_id,
                                options=control_options,
                                value=control_default,
                                style={"minWidth": "200px"}
                            )
                        ],
                        style={"marginBottom": "15px"}
                    ),
                    width=6
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='chart2-graph',
                        style={'height': '80vh'},
                        config={'responsive': True}
                    ),
                    width=12
                ),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
    className="page-content"
)


@callback(
    Output('chart2-graph', 'figure'),
    Input(control_id, 'value')
)
def update_chart(color_by):
    """Update the choropleth map based on user input."""
    return create_choropleth_figure(color_by or control_default)
