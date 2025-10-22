"""
Home Page - Geopolitical Threat Perception Density Map
"""

import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import sys
import os

# Register this page
dash.register_page(__name__, path='/')

# Import the geopolitical app function
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from geopolitical_app import create_threat_density_map

# Create the layout
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H1(
                                "Central Asian Regional Threat Perception Analysis",
                                className="page-title"
                            ),
                            html.P(
                                "Geopolitical threat perception density map showing military spending and regional distance metrics",
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
                    dcc.Graph(
                        id='threat-perception-graph',
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

# Callback to generate the figure
@callback(
    Output('threat-perception-graph', 'figure'),
    Input('threat-perception-graph', 'id')
)
def update_graph(_):
    """Generate the threat perception map"""
    return create_threat_density_map()

