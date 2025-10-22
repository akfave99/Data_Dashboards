"""
Multi-Page Geopolitical Analysis Dashboard
Built with Plotly Dash and Bootstrap Components
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

# Create the Dash app with multi-page support
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.SLATE,
        '/assets/custom.css'
    ]
)

# Define the navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Threat Perception", href="/")),
        dbc.NavItem(dbc.NavLink("Supplier Influence Surface", href="/chart1")),
        dbc.NavItem(dbc.NavLink("Regional Influence Map", href="/chart2")),
        dbc.NavItem(dbc.NavLink("Defense Systems Analysis", href="/chart3")),
        dbc.NavItem(dbc.NavLink("Multi-Country Radar", href="/chart4")),
        dbc.NavItem(dbc.NavLink("Priorities Heatmap", href="/chart5")),
        dbc.NavItem(dbc.NavLink("Regional Density", href="/chart6")),
        dbc.NavItem(dbc.NavLink("Supplier Connections", href="/chart7")),
    ],
    brand="Geopolitical Analysis Dashboard",
    brand_href="/",
    color="dark",
    dark=True,
    sticky="top",
)

# Define the footer
footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        html.P("© 2025 Geopolitical Analysis Dashboard | Built with Plotly Dash", className="footer-text"),
                        html.P("Created by: A.K. Faver on October 21, 2025.", className="footer-text", style={"fontSize": "0.9em", "marginTop": "5px"})
                    ],
                    style={"textAlign": "center"}
                ),
                align="center"
            ),
        ],
    ),
    className="footer",
    fluid=True,
)

# Overall layout
app.layout = html.Div([
    navbar,
    html.Div(
        dash.page_container,
        className="page-container"
    ),
    footer,
])

# Get the server for deployment
server = app.server

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True, port=8050)
