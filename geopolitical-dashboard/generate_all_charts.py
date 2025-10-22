"""
Generate all charts as individual HTML files
"""

import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import plotly.express as px
from geopolitical_app import create_threat_density_map
from chart_data import get_data
import numpy as np
import pandas as pd

# Load environment variables
load_dotenv()

def create_chart1():
    """Supplier Influence Surface"""
    data = get_data()
    
    # Create 3D surface
    x = np.linspace(0, 10, 50)
    y = np.linspace(0, 10, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y) * 100
    
    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')])
    fig.update_layout(
        title="Supplier Influence Surface",
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Influence"),
        height=700
    )
    return fig

def create_chart2():
    """Regional Influence Map"""
    data = get_data()
    
    fig = px.scatter_geo(data, 
                         lat='Latitude', 
                         lon='Longitude',
                         hover_name='Country',
                         size='Avg_Spend',
                         color='Threat_Level',
                         title="Regional Influence Map",
                         projection="natural earth")
    fig.update_layout(height=700)
    return fig

def create_chart3():
    """Defense Systems Analysis"""
    data = get_data()
    
    fig = go.Figure()
    for country in data['Country'].unique():
        country_data = data[data['Country'] == country]
        fig.add_trace(go.Scatterpolar(
            r=country_data['Avg_Spend'].values,
            theta=['Defense', 'Cyber', 'Naval', 'Air', 'Ground'],
            fill='toself',
            name=country
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 150000000])),
        title="Defense Systems Analysis",
        height=700
    )
    return fig

def create_chart4():
    """Multi-Country Radar"""
    data = get_data()
    
    fig = go.Figure()
    for country in data['Country'].unique()[:3]:
        fig.add_trace(go.Scatterpolar(
            r=np.random.rand(6) * 100,
            theta=['A', 'B', 'C', 'D', 'E', 'F'],
            fill='toself',
            name=country
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="Multi-Country Radar",
        height=700
    )
    return fig

def create_chart5():
    """Priorities Heatmap"""
    data = get_data()
    
    heatmap_data = np.random.rand(5, 5) * 100
    fig = go.Figure(data=go.Heatmap(z=heatmap_data, colorscale='RdYlGn'))
    fig.update_layout(
        title="Priorities Heatmap",
        xaxis_title="Priority",
        yaxis_title="Country",
        height=700
    )
    return fig

def create_chart6():
    """Regional Density"""
    data = get_data()
    
    fig = px.density_mapbox(data,
                            lat='Latitude',
                            lon='Longitude',
                            hover_name='Country',
                            title="Regional Density",
                            mapbox_style="open-street-map")
    fig.update_layout(height=700)
    return fig

def create_chart7():
    """Supplier Connections"""
    data = get_data()
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=data['Country'].tolist()
        ),
        link=dict(
            source=[0, 1, 2],
            target=[1, 2, 3],
            value=[10, 20, 30]
        )
    )])
    fig.update_layout(title="Supplier Connections", height=700)
    return fig

def main():
    print("=" * 70)
    print("GENERATING ALL CHARTS AS HTML")
    print("=" * 70)
    print()
    
    charts = [
        ("Chart 0: Threat Perception", create_threat_density_map, "threat-perception-analysis"),
        ("Chart 1: Supplier Influence Surface", create_chart1, "chart1-supplier-influence"),
        ("Chart 2: Regional Influence Map", create_chart2, "chart2-regional-influence"),
        ("Chart 3: Defense Systems Analysis", create_chart3, "chart3-defense-systems"),
        ("Chart 4: Multi-Country Radar", create_chart4, "chart4-multi-country-radar"),
        ("Chart 5: Priorities Heatmap", create_chart5, "chart5-priorities-heatmap"),
        ("Chart 6: Regional Density", create_chart6, "chart6-regional-density"),
        ("Chart 7: Supplier Connections", create_chart7, "chart7-supplier-connections"),
    ]
    
    generated_files = []
    
    for title, chart_func, filename in charts:
        try:
            print(f"📊 {title}")
            fig = chart_func()
            html_file = f"{filename}.html"
            fig.write_html(html_file)
            generated_files.append((title, html_file))
            print(f"   ✅ Saved: {html_file}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
    
    print("=" * 70)
    print(f"✅ GENERATED {len(generated_files)} CHARTS")
    print("=" * 70)
    print()
    print("Generated files:")
    for title, filename in generated_files:
        print(f"  - {filename}")

if __name__ == '__main__':
    main()
