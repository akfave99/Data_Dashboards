"""
Wrap exported charts with navigation tabs and copy to docs folder
"""

import os
import re
import shutil

def wrap_chart_with_navigation(chart_file, chart_id, chart_title):
    """Wrap existing chart HTML with navigation and styling"""
    
    with open(chart_file, 'r', encoding='utf-8', errors='ignore') as f:
        original_html = f.read()
    
    # Extract everything between <body> and </body>
    body_match = re.search(r'<body[^>]*>(.*?)</body>', original_html, re.DOTALL)
    body_content = body_match.group(1) if body_match else ""
    
    # Extract head content (scripts, styles)
    head_match = re.search(r'<head[^>]*>(.*?)</head>', original_html, re.DOTALL)
    head_content = head_match.group(1) if head_match else ""
    
    # Navigation HTML
    nav_html = '''
    <nav class="navbar">
        <div class="navbar-container">
            <a class="navbar-brand" href="index.html">🌍 Geopolitical Dashboard</a>
            <div class="nav-tabs">
                <a href="threat-perception-analysis.html" class="nav-tab''' + (' active' if chart_id == 'threat' else '') + '''">Threat Perception</a>
                <a href="chart1-supplier-influence.html" class="nav-tab''' + (' active' if chart_id == 'chart1' else '') + '''">Supplier Influence</a>
                <a href="chart3-defense-systems.html" class="nav-tab''' + (' active' if chart_id == 'chart3' else '') + '''">Defense Systems</a>
                <a href="chart4-multi-country-radar.html" class="nav-tab''' + (' active' if chart_id == 'chart4' else '') + '''">Multi-Country Radar</a>
                <a href="chart5-priorities-heatmap.html" class="nav-tab''' + (' active' if chart_id == 'chart5' else '') + '''">Priorities Heatmap</a>
                <a href="chart7-supplier-connections.html" class="nav-tab''' + (' active' if chart_id == 'chart7' else '') + '''">Supplier Connections</a>
            </div>
        </div>
    </nav>
    '''
    
    # Create wrapper HTML
    wrapper_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chart_title} | Geopolitical Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: linear-gradient(135deg, #0d1b2a 0%, #1a1a2e 100%);
            color: #fff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }}
        
        .navbar {{
            background-color: #0d1b2a;
            border-bottom: 2px solid #1e90ff;
            padding: 15px 20px;
            box-shadow: 0 2px 10px rgba(30, 144, 255, 0.2);
        }}
        
        .navbar-container {{
            max-width: 100%;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }}
        
        .navbar-brand {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #1e90ff;
            text-decoration: none;
            white-space: nowrap;
        }}
        
        .navbar-brand:hover {{
            color: #00d4ff;
        }}
        
        .nav-tabs {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            justify-content: flex-end;
        }}
        
        .nav-tab {{
            padding: 8px 15px;
            background-color: #1a1a2e;
            border: 1px solid #1e90ff;
            border-radius: 4px;
            color: #aaa;
            text-decoration: none;
            font-size: 0.85rem;
            transition: all 0.3s;
            white-space: nowrap;
        }}
        
        .nav-tab:hover {{
            background-color: #1e90ff;
            color: #fff;
            border-color: #00d4ff;
        }}
        
        .nav-tab.active {{
            background-color: #1e90ff;
            color: #fff;
            border-color: #00d4ff;
        }}
        
        .content-container {{
            padding: 20px;
            max-width: 100%;
        }}
        
        .footer {{
            background-color: #0d1b2a;
            border-top: 2px solid #1e90ff;
            padding: 20px;
            text-align: center;
            color: #aaa;
            margin-top: 40px;
        }}
        
        @media (max-width: 768px) {{
            .navbar-container {{
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .nav-tabs {{
                justify-content: flex-start;
                width: 100%;
            }}
            
            .nav-tab {{
                flex: 1;
                text-align: center;
                min-width: 100px;
            }}
        }}
    </style>
    {head_content}
</head>
<body>
    {nav_html}
    <div class="content-container">
        {body_content}
    </div>
    <div class="footer">
        <p>© 2025 Geopolitical Analysis Dashboard</p>
    </div>
</body>
</html>'''
    
    return wrapper_html

def main():
    print("=" * 70)
    print("WRAPPING CHARTS WITH NAVIGATION")
    print("=" * 70)
    print()
    
    charts = [
        ("threat-perception-analysis.html", "threat", "Threat Perception Analysis"),
        ("chart1-supplier-influence.html", "chart1", "Supplier Influence"),
        ("chart3-defense-systems.html", "chart3", "Defense Systems Analysis"),
        ("chart4-multi-country-radar.html", "chart4", "Multi-Country Radar"),
        ("chart5-priorities-heatmap.html", "chart5", "Priorities Heatmap"),
        ("chart7-supplier-connections.html", "chart7", "Supplier Connections"),
    ]
    
    for chart_file, chart_id, chart_title in charts:
        try:
            print(f"📊 Wrapping {chart_title}...")
            wrapped_html = wrap_chart_with_navigation(chart_file, chart_id, chart_title)
            
            # Write wrapped version back
            with open(chart_file, 'w', encoding='utf-8') as f:
                f.write(wrapped_html)
            
            print(f"   ✅ Wrapped: {chart_file}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
        print()
    
    print("=" * 70)
    print("COPYING CHARTS TO DOCS FOLDER")
    print("=" * 70)
    print()
    
    docs_folder = "../docs"
    os.makedirs(docs_folder, exist_ok=True)
    
    for chart_file, _, _ in charts:
        try:
            dest = os.path.join(docs_folder, chart_file)
            shutil.copy(chart_file, dest)
            print(f"✅ Copied {chart_file} to {dest}")
        except Exception as e:
            print(f"❌ Error copying {chart_file}: {e}")
    
    print()
    print("=" * 70)
    print("✅ ALL CHARTS WRAPPED AND DEPLOYED")
    print("=" * 70)

if __name__ == '__main__':
    main()
