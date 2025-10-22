"""
Upload individual charts to Plotly Cloud
"""

import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import plotly.express as px
from geopolitical_app import create_threat_density_map
from chart_data import get_data
import plotly.io as pio

# Load environment variables from .env file
load_dotenv()

# Get credentials from .env file
PLOTLY_USERNAME = os.getenv('PLOTLY_USERNAME')
PLOTLY_API_KEY = os.getenv('PLOTLY_API_KEY')

if not PLOTLY_USERNAME or not PLOTLY_API_KEY:
    print("❌ ERROR: PLOTLY_USERNAME or PLOTLY_API_KEY not found in .env file")
    print("Please create a .env file with:")
    print("  PLOTLY_USERNAME=your_username")
    print("  PLOTLY_API_KEY=your_api_key")
    exit(1)

def upload_chart(figure, filename, description=""):
    """Save chart as HTML for uploading to Plotly Cloud"""
    try:
        html_file = f"{filename}.html"
        figure.write_html(html_file)
        print(f"✅ Saved: {html_file}")
        return html_file
    except Exception as e:
        print(f"❌ Error creating {filename}: {e}")
        return None

def main():
    print("=" * 70)
    print("PREPARING CHARTS FOR PLOTLY CLOUD")
    print("=" * 70)
    print()
    
    # Chart 0: Threat Perception (Home)
    print("📊 Chart 0: Central Asian Regional Threat Perception Analysis")
    try:
        fig_home = create_threat_density_map()
        upload_chart(fig_home, "threat-perception-analysis")
    except Exception as e:
        print(f"❌ Error creating chart: {e}")
    print()
    
    print("=" * 70)
    print("✅ CHARTS READY!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Go to https://chart-studio.plotly.com/")
    print("2. Click 'Create' → 'Chart'")
    print("3. Upload the HTML files")
    print("4. Create a dashboard and add your charts")
    print("5. Publish!")

if __name__ == '__main__':
    main()
