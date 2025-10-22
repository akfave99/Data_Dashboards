"""
Create a simple multi-page HTML dashboard with direct links
"""

def create_dashboard_html():
    """Create the main dashboard HTML with navigation"""
    
    charts = [
        {
            "name": "Threat Perception",
            "file": "threat-perception-analysis.html",
            "description": "Central Asian Regional Threat Perception Analysis"
        },
        {
            "name": "Supplier Influence",
            "file": "chart1-supplier-influence.html",
            "description": "Defense Supplier Influence 3D Surface"
        },
        {
            "name": "Defense Systems",
            "file": "chart3-defense-systems.html",
            "description": "Defense Systems Analysis"
        },
        {
            "name": "Multi-Country Radar",
            "file": "chart4-multi-country-radar.html",
            "description": "Multi-Country Radar Comparison"
        },
        {
            "name": "Priorities Heatmap",
            "file": "chart5-priorities-heatmap.html",
            "description": "Defense Priorities Heatmap"
        },
        {
            "name": "Supplier Connections",
            "file": "chart7-supplier-connections.html",
            "description": "Supplier Connections Sankey Diagram"
        },
    ]
    
    # Create navigation HTML
    nav_items = ""
    for i, chart in enumerate(charts):
        nav_items += f'                <li class="nav-item"><a class="nav-link" href="{chart["file"]}">{chart["name"]}</a></li>\n'
    
    # Create index/home page
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Geopolitical Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #0d1b2a 0%, #1a1a2e 100%);
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }}
        .navbar {{
            background-color: #0d1b2a;
            border-bottom: 2px solid #1e90ff;
        }}
        .navbar-brand {{
            font-weight: bold;
            font-size: 1.5rem;
            color: #1e90ff !important;
        }}
        .nav-link {{
            color: #aaa !important;
            transition: color 0.3s;
            margin: 0 5px;
        }}
        .nav-link:hover {{
            color: #1e90ff !important;
        }}
        .hero {{
            text-align: center;
            padding: 60px 20px;
        }}
        .hero h1 {{
            font-size: 3rem;
            font-weight: bold;
            color: #1e90ff;
            margin-bottom: 20px;
            text-shadow: 0 2px 10px rgba(30, 144, 255, 0.3);
        }}
        .hero p {{
            font-size: 1.3rem;
            color: #aaa;
            margin-bottom: 40px;
        }}
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 40px 20px;
        }}
        .chart-card {{
            background-color: #0d1b2a;
            border: 2px solid #1e90ff;
            border-radius: 8px;
            padding: 20px;
            transition: all 0.3s;
            cursor: pointer;
            text-decoration: none;
            color: #fff;
        }}
        .chart-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(30, 144, 255, 0.3);
            border-color: #00d4ff;
        }}
        .chart-card h3 {{
            color: #1e90ff;
            margin-bottom: 10px;
        }}
        .chart-card p {{
            color: #aaa;
            font-size: 0.95rem;
        }}
        .footer {{
            background-color: #0d1b2a;
            border-top: 2px solid #1e90ff;
            padding: 20px;
            text-align: center;
            color: #aaa;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="index.html">🌍 Geopolitical Dashboard</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
{nav_items}                </ul>
            </div>
        </div>
    </nav>

    <div class="hero">
        <h1>🌍 Geopolitical Analysis Dashboard</h1>
        <p>Central Asian Regional Threat Perception & Defense Analysis</p>
    </div>

    <div class="container-fluid">
        <div class="charts-grid">
"""
    
    for i, chart in enumerate(charts):
        index_html += f"""            <a href="{chart["file"]}" class="chart-card">
                <h3>{chart["name"]}</h3>
                <p>{chart["description"]}</p>
            </a>
"""
    
    index_html += """        </div>
    </div>

    <div class="footer">
        <p>© 2025 Geopolitical Analysis Dashboard | Built with Plotly & Bootstrap</p>
        <p>Created by: A.K. Faver</p>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
    
    with open("index.html", "w") as f:
        f.write(index_html)
    print("✅ Created index.html - Dashboard Home")

if __name__ == '__main__':
    print("=" * 70)
    print("CREATING SIMPLE MULTI-PAGE HTML DASHBOARD")
    print("=" * 70)
    print()
    create_dashboard_html()
    print()
    print("=" * 70)
    print("✅ DASHBOARD CREATED!")
    print("=" * 70)
