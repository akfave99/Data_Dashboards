"""
Chart 7 Page - Supplier-Receiver Connection Map
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

dash.register_page(__name__, path='/chart7', name='Supplier Connections')

component_id = "supplier_receiver_connection_map"
supplier_selector_id = f"{component_id}_supplier"

def create_connection_map_figure(selected_supplier="all"):
    """Create supplier-receiver connection map."""
    df = filter_data(get_data())

    if len(df) == 0:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No data available",
            annotations=[{"text": "No data available", "showarrow": False}]
        )
        return empty_fig

    suppliers = ['US', 'Russia', 'China', 'Turkiye_Israel']
    supplier_labels = ['United States', 'Russia', 'China', 'Türkiye/Israel']

    # Create nodes for suppliers and receivers (countries)
    nodes = supplier_labels + df['Country'].tolist()
    node_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'] + ['#9467bd'] * len(df)

    # Create edges (connections)
    source = []
    target = []
    value = []

    for idx, supplier in enumerate(suppliers):
        if selected_supplier != "all" and supplier != selected_supplier:
            continue

        influence_col = f'Influence_{supplier}_numeric'

        for country_idx, (_, row) in enumerate(df.iterrows()):
            influence = row.get(influence_col, 0)
            if pd.notna(influence) and influence > 0:
                source.append(idx)
                target.append(len(supplier_labels) + country_idx)
                value.append(float(influence) * 10)  # Scale for visibility

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=nodes,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=['rgba(31, 119, 180, 0.4)' if s == 0 else
                   'rgba(255, 127, 14, 0.4)' if s == 1 else
                   'rgba(44, 160, 44, 0.4)' if s == 2 else
                   'rgba(214, 39, 40, 0.4)' for s in source]
        )
    )])

    fig.update_layout(
        title=f"Supplier-Receiver Connection Map" + (f" ({supplier_labels[suppliers.index(selected_supplier)]})" if selected_supplier != "all" else ""),
        font=dict(size=12),
        height=700
    )

    return fig

# Get suppliers for dropdown
suppliers = ['US', 'Russia', 'China', 'Turkiye_Israel']
supplier_labels = ['United States', 'Russia', 'China', 'Türkiye/Israel']
supplier_options = [{"label": "All Suppliers", "value": "all"}] + [
    {"label": label, "value": supplier} for supplier, label in zip(suppliers, supplier_labels)
]

layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.Div([
                html.H1("Defense Supplier-Receiver Connection Map", className="page-title"),
                html.P("Sankey diagram illustrating the flow of defense supplier relationships with recipient countries. Left nodes represent defense suppliers (US, Russia, China, Türkiye/Israel), color-coded for easy identification. Right nodes show recipient countries. Flow width represents the strength of the relationship (influence level). Select individual suppliers to focus on specific relationships, or view all suppliers simultaneously to understand the complete network of defense connections.", className="page-subtitle"),
            ]), width=12),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                html.Label("Select Supplier:", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id=supplier_selector_id,
                    options=supplier_options,
                    value="all",
                    style={"minWidth": "200px"}
                ),
            ], width=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='chart7-graph', style={'height': '80vh'}, config={'responsive': True}), width=12),
        ], className="mb-4"),
    ],
    fluid=True,
    className="page-content"
)

@callback(
    Output('chart7-graph', 'figure'),
    Input(supplier_selector_id, 'value')
)
def update_chart(selected_supplier):
    return create_connection_map_figure(selected_supplier or "all")
