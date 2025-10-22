"""
Chart 3 Page - Defense Systems 3D Analysis by Supplier
"""

import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import sys
import os

dash.register_page(__name__, path='/chart3', name='Defense Systems Analysis')

# Import data module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chart_data import get_data, filter_data

# Component configuration
component_id = "defense_systems_3d_scatter"
supplier_control_id = f"{component_id}_supplier"

supplier_options = [
    {"label": "All Suppliers", "value": "all"},
    {"label": "United States", "value": "US"},
    {"label": "Russia", "value": "Russia"},
    {"label": "China", "value": "China"},
    {"label": "Türkiye/Israel", "value": "Turkiye_Israel"}
]
supplier_default = "all"


def create_3d_scatter_figure(supplier_filter="all"):
    """Create the 3D scatter plot."""
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

    plot_data = []
    
    for _, row in df.iterrows():
        country = row['Country']
        suppliers_data = [
            ('US', row.get('Systems_US'), row.get('Influence_US_numeric', 0)),
            ('Russia', row.get('Systems_Russia'), row.get('Influence_Russia_numeric', 0)),
            ('China', row.get('Systems_China'), row.get('Influence_China_numeric', 0)),
            ('Turkiye_Israel', row.get('Systems_Turkiye_Israel'), row.get('Influence_Turkiye_Israel_numeric', 0))
        ]
        
        for supplier, systems, influence in suppliers_data:
            if pd.isna(systems) or systems == '' or systems == 'N/A':
                continue
            if supplier_filter != "all" and supplier != supplier_filter:
                continue
            system_count = len([s.strip() for s in str(systems).replace(';', ',').split(',') if s.strip()])
            plot_data.append({
                'Country': country,
                'Supplier': supplier,
                'System_Count': system_count,
                'Influence': influence if not pd.isna(influence) else 0,
                'Systems': systems,
                'Threat_Perception': row.get('Threat Perception', ''),
                'Defense_Priorities': row.get('Defense Priorities', '')
            })
    
    if not plot_data:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No data available for selected supplier",
            annotations=[{
                "text": "No defense systems data available for the selected supplier filter",
                "showarrow": False,
                "font": {"size": 16}
            }]
        )
        return empty_fig
    
    plot_df = pd.DataFrame(plot_data)
    countries = plot_df['Country'].unique()
    country_mapping = {country: i for i, country in enumerate(countries)}
    plot_df['Country_Z'] = plot_df['Country'].map(country_mapping)
    
    supplier_colors = {
        'US': '#1f77b4',
        'Russia': '#d62728', 
        'China': '#ff7f0e',
        'Turkiye_Israel': '#2ca02c'
    }
    
    fig = go.Figure()
    
    for supplier in plot_df['Supplier'].unique():
        supplier_data = plot_df[plot_df['Supplier'] == supplier]
        supplier_display = {
            'US': 'United States',
            'Russia': 'Russia', 
            'China': 'China',
            'Turkiye_Israel': 'Türkiye/Israel'
        }.get(supplier, supplier)
        
        fig.add_trace(go.Scatter3d(
            x=supplier_data['System_Count'],
            y=supplier_data['Influence'],
            z=supplier_data['Country_Z'],
            mode='markers',
            marker=dict(
                size=supplier_data['Influence'] * 3 + 5,
                color=supplier_colors.get(supplier, '#636EFA'),
                opacity=0.8,
                line=dict(width=1, color='white')
            ),
            name=supplier_display,
            text=supplier_data['Country'],
            customdata=supplier_data[['Systems', 'Threat_Perception', 'Defense_Priorities']],
            hovertemplate=(
                "<b>%{text}</b><br>" +
                f"Supplier: {supplier_display}<br>" +
                "System Count: %{x}<br>" +
                "Influence Level: %{y}<br>" +
                "Systems: %{customdata[0]}<br>" +
                "<extra></extra>"
            )
        ))
    
    fig.update_layout(
        scene=dict(
            xaxis_title="Number of Defense Systems",
            yaxis_title="Influence Level (1-3)",
            zaxis_title="Countries",
            zaxis=dict(
                tickmode='array',
                tickvals=list(range(len(countries))),
                ticktext=countries
            ),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
        margin=dict(l=0, r=0, t=30, b=0),
        height=700
    )

    return fig


layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.Div([
                html.H1("Defense Systems 3D Analysis by Supplier", className="page-title"),
                html.P("3D scatter plot analyzing the relationship between defense systems, supplier influence, and countries. X-axis shows the number of defense systems, Y-axis represents influence level (1-3), and Z-axis displays countries. Point size is proportional to influence level. Filter by supplier to focus on specific defense relationships.", className="page-subtitle"),
            ]), width=12),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(html.Div([
                html.Label("Supplier Filter:", style={"fontWeight": "bold"}),
                dcc.Dropdown(id=supplier_control_id, options=supplier_options, value=supplier_default, style={"minWidth": "200px"})
            ], style={"marginBottom": "15px"}), width=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='chart3-graph', style={'height': '80vh'}, config={'responsive': True}), width=12),
        ], className="mb-4"),
    ],
    fluid=True,
    className="page-content"
)


@callback(Output('chart3-graph', 'figure'), Input(supplier_control_id, 'value'))
def update_chart(supplier_filter):
    return create_3d_scatter_figure(supplier_filter or supplier_default)
