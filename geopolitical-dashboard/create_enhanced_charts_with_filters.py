"""
Enhanced Chart Generation Script with Filters and Navigation
Generates HTML charts with embedded interactive filters and navigation tabs
"""

import os
import json
from pages.chart1 import create_3d_surface_figure
from pages.chart2 import create_choropleth_figure
from pages.chart3 import create_3d_scatter_figure
from pages.chart4 import create_radar_figure
from pages.chart5 import create_heatmap_figure
from pages.chart7 import create_connection_map_figure
from geopolitical_app import create_threat_density_map
import plotly.io as pio

# Chart definitions
CHARTS = [
    {
        "id": "threat-perception-analysis",
        "title": "Central Asian Regional Threat Perception Analysis",
        "description": "3D density map with flag images showing threat perception and military spending",
        "function": create_threat_density_map,
        "filters": []
    },
    {
        "id": "chart1-supplier-influence",
        "title": "Defense Supplier Influence",
        "description": "3D Surface visualization of supplier influence across countries",
        "function": create_3d_surface_figure,
        "filters": [
            {
                "name": "influence_type",
                "label": "Influence Type:",
                "type": "dropdown",
                "options": [
                    {"label": "Influence", "value": "Influence"},
                    {"label": "Matrix", "value": "Matrix"}
                ],
                "default": "Influence"
            }
        ]
    },
    {
        "id": "chart3-defense-systems",
        "title": "Defense Systems Analysis",
        "description": "3D scatter plot of defense systems by supplier",
        "function": create_3d_scatter_figure,
        "filters": [
            {
                "name": "supplier_filter",
                "label": "Select Supplier:",
                "type": "dropdown",
                "options": [
                    {"label": "All Suppliers", "value": "all"},
                    {"label": "US", "value": "US"},
                    {"label": "Russia", "value": "Russia"},
                    {"label": "China", "value": "China"}
                ],
                "default": "all"
            }
        ]
    },
    {
        "id": "chart4-multi-country-radar",
        "title": "Multi-Country Radar Comparison",
        "description": "Radar chart comparing multiple countries across metrics",
        "function": create_radar_figure,
        "filters": [
            {
                "name": "metric_type",
                "label": "Select Metric Type:",
                "type": "dropdown",
                "options": [
                    {"label": "Influence Metrics", "value": "influence"},
                    {"label": "Matrix Metrics", "value": "matrix"}
                ],
                "default": "influence"
            }
        ]
    },
    {
        "id": "chart5-priorities-heatmap",
        "title": "Defense Priorities Heatmap",
        "description": "Heatmap showing defense priorities across countries",
        "function": create_heatmap_figure,
        "filters": []
    },
    {
        "id": "chart7-supplier-connections",
        "title": "Supplier Connections",
        "description": "Sankey diagram showing supplier connections",
        "function": create_connection_map_figure,
        "filters": [
            {
                "name": "selected_supplier",
                "label": "Select Supplier:",
                "type": "dropdown",
                "options": [
                    {"label": "All Suppliers", "value": "all"},
                    {"label": "US", "value": "US"},
                    {"label": "Russia", "value": "Russia"},
                    {"label": "China", "value": "China"}
                ],
                "default": "all"
            }
        ]
    }
]

def generate_all_charts():
    """Generate all enhanced charts"""
    print("=" * 70)
    print("GENERATING ENHANCED CHARTS WITH FILTERS AND NAVIGATION")
    print("=" * 70)
    
    for i, chart_def in enumerate(CHARTS, 1):
        try:
            print(f"\n[{i}/{len(CHARTS)}] Generating {chart_def['title']}...")
            
            # Generate the figure
            if chart_def["id"] == "threat-perception-analysis":
                fig = chart_def["function"]()
            elif chart_def["id"] == "chart1-supplier-influence":
                fig = chart_def["function"]("Influence", True)
            elif chart_def["id"] == "chart3-defense-systems":
                fig = chart_def["function"]("all")
            elif chart_def["id"] == "chart4-multi-country-radar":
                fig = chart_def["function"](None, "influence")
            elif chart_def["id"] == "chart5-priorities-heatmap":
                fig = chart_def["function"]()
            elif chart_def["id"] == "chart7-supplier-connections":
                fig = chart_def["function"]("all")
            
            print(f"✅ Generated: {chart_def['id']}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    generate_all_charts()
