"""
Export charts from the Dash app pages as standalone HTML files
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from geopolitical_app import create_threat_density_map
from pages.chart1 import create_3d_surface_figure
from pages.chart3 import create_3d_scatter_figure
from pages.chart4 import create_radar_figure
from pages.chart5 import create_heatmap_figure
from pages.chart7 import create_connection_map_figure

def main():
    print("=" * 70)
    print("EXPORTING CHARTS FROM DASH APP")
    print("=" * 70)
    print()
    
    charts = [
        ("Chart 0: Threat Perception", create_threat_density_map, "threat-perception-analysis", {}),
        ("Chart 1: Supplier Influence", create_3d_surface_figure, "chart1-supplier-influence", {"influence_type": "Influence", "show_all_countries": True}),
        ("Chart 3: Defense Systems", create_3d_scatter_figure, "chart3-defense-systems", {"supplier_filter": "all"}),
        ("Chart 4: Multi-Country Radar", create_radar_figure, "chart4-multi-country-radar", {"selected_countries": None, "metric_type": "influence"}),
        ("Chart 5: Priorities Heatmap", create_heatmap_figure, "chart5-priorities-heatmap", {"grouping": "country", "intensity_metric": "influence"}),
        ("Chart 7: Supplier Connections", create_connection_map_figure, "chart7-supplier-connections", {"selected_supplier": "all"}),
    ]
    
    generated_files = []
    
    for title, chart_func, filename, kwargs in charts:
        try:
            print(f"📊 {title}")
            fig = chart_func(**kwargs)
            html_file = f"{filename}.html"
            fig.write_html(html_file)
            generated_files.append((title, html_file))
            print(f"   ✅ Saved: {html_file}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
        print()
    
    print("=" * 70)
    print(f"✅ EXPORTED {len(generated_files)} CHARTS")
    print("=" * 70)

if __name__ == '__main__':
    main()
