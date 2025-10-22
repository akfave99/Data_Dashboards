"""
Chart 1 Page - Defense Supplier Influence 3D Surface
"""

import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys
import os

# Register this page
dash.register_page(__name__, path='/chart1', name='Supplier Influence Surface')

# Import data module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chart_data import get_data, filter_data

# Component configuration
component_id = "defense_supplier_influence_3d_surface"
influence_type_id = f"{component_id}_influence_type"
country_toggle_id = f"{component_id}_country_toggle"

influence_type_options = [
    {"label": "Influence", "value": "Influence"},
    {"label": "Matrix", "value": "Matrix"}
]
influence_type_default = "Influence"


def create_3d_surface_figure(influence_type="Influence", show_all_countries=True):
    """Create the 3D surface chart."""
    df = filter_data(get_data())

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

    if not show_all_countries and len(df) > 0:
        df = df.head(3)

    suppliers = ["US", "Russia", "China", "Turkiye_Israel"]
    countries = df["Country"].tolist()

    z_data = []
    for country in countries:
        country_data = df[df["Country"] == country]
        if len(country_data) == 0:
            z_row = [0, 0, 0, 0]
        else:
            z_row = []
            for supplier in suppliers:
                col_name = f"{influence_type}_{supplier}_numeric"
                if col_name in country_data.columns:
                    value = country_data[col_name].iloc[0]
                    if pd.isna(value):
                        z_row.append(0)
                    else:
                        z_row.append(float(value))
                else:
                    z_row.append(0)
        z_data.append(z_row)

    if len(z_data) == 0:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No data available for surface plot",
            annotations=[{
                "text": "Insufficient data for 3D surface visualization",
                "showarrow": False,
                "font": {"size": 20}
            }]
        )
        return empty_fig

    z_array = np.array(z_data)

    x_labels = ["US", "Russia", "China", "Türkiye/Israel"]
    y_labels = countries

    fig = go.Figure(data=[go.Surface(
        z=z_array,
        x=list(range(len(x_labels))),
        y=list(range(len(y_labels))),
        colorscale='Viridis',
        hovertemplate="<b>%{text}</b><br>" +
                      "Supplier: %{customdata[0]}<br>" +
                      "Country: %{customdata[1]}<br>" +
                      f"{influence_type} Level: %{{z:.1f}}<br>" +
                      "<extra></extra>",
        text=[[f"{y_labels[j]} - {x_labels[i]}" for i in range(len(x_labels))] for j in range(len(y_labels))],
        customdata=[[[x_labels[i], y_labels[j]] for i in range(len(x_labels))] for j in range(len(y_labels))]
    )])

    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title="Defense Suppliers",
                tickmode='array',
                tickvals=list(range(len(x_labels))),
                ticktext=x_labels
            ),
            yaxis=dict(
                title="Countries",
                tickmode='array',
                tickvals=list(range(len(y_labels))),
                ticktext=y_labels
            ),
            zaxis=dict(
                title=f"{influence_type} Level"
            ),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=700
    )

    return fig


# Create the layout
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H1(
                                "Defense Supplier Influence Surface Analysis",
                                className="page-title"
                            ),
                            html.P(
                                "3D surface visualization showing how defense suppliers (US, Russia, China, Türkiye/Israel) influence different Central Asian countries. The height of the surface represents the influence level (1-3 scale), allowing you to identify patterns and compare supplier influence across the region.",
                                className="page-subtitle"
                            ),
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
                            html.Label("Influence Type:", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id=influence_type_id,
                                options=influence_type_options,
                                value=influence_type_default,
                                style={"minWidth": "200px"}
                            )
                        ],
                        style={"marginBottom": "15px"}
                    ),
                    width=6
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Label("Show All Countries:", style={"fontWeight": "bold"}),
                            dcc.Checklist(
                                id=country_toggle_id,
                                options=[{"label": " Enabled", "value": "enabled"}],
                                value=["enabled"],
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
                        id='chart1-graph',
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
    Output('chart1-graph', 'figure'),
    [
        Input(influence_type_id, 'value'),
        Input(country_toggle_id, 'value')
    ]
)
def update_chart(influence_type, country_toggle):
    """Update the 3D surface chart based on user inputs."""
    show_all = 'enabled' in (country_toggle or [])
    return create_3d_surface_figure(influence_type or influence_type_default, show_all)

