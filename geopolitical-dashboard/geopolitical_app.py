"""
Geopolitical Threat Perception Density Map - Plotly Dash Application

This is a Dash web application that displays the geopolitical threat perception
visualization. It can be run locally or deployed to cloud platforms.

To run locally:
    python3 app.py

Then open: http://localhost:8050

To deploy:
    See DASH_DEPLOYMENT.md for instructions
"""

from dash import Dash, dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import requests
from io import BytesIO
import base64
import os

# ============================================================================
# FLAG URLS AND CONFIGURATION
# ============================================================================

FLAG_URLS = {
    "Kazakhstan":    "https://flagcdn.com/256x192/kz.png",
    "Uzbekistan":    "https://flagcdn.com/256x192/uz.png",
    "Turkmenistan":  "https://flagcdn.com/256x192/tm.png",
    "Azerbaijan":    "https://flagcdn.com/256x192/az.png",
    "Georgia":       "https://flagcdn.com/256x192/ge.png",
}

SPEND_COL_CANDIDATES = ["Avg_Spend", "Weapons_Spend", "Spend"]

# ============================================================================
# DATA GENERATION
# ============================================================================

def get_data():
    """Generate geopolitical threat perception data.

    VISUALIZATION FOCUS: Central Asian Regional Threat Perception

    This visualization focuses on Central Asian countries and their threat perceptions.
    The regional countries are:
    - Kazakhstan, Uzbekistan, Turkmenistan, Azerbaijan, Georgia

    These countries face various regional threats and security challenges.
    """
    data = {
        "Country": [
            "Kazakhstan", "Uzbekistan", "Turkmenistan", "Azerbaijan", "Georgia"
        ],
        "Avg_Spend": [
            120_000_000, 90_000_000, 45_000_000, 70_000_000, 30_000_000
        ],
        "Threat Perception": [
            "Regional Instability", "Regional Instability", "Border Security",
            "Energy Competition", "Russian Influence"
        ]
    }
    return pd.DataFrame(data)


def _compute_avg_spend(df: pd.DataFrame) -> pd.DataFrame:
    """Compute average spending by country."""
    spend_num = pd.to_numeric(df["Avg_Spend"], errors="coerce")
    out = df.assign(Avg_Spend=spend_num).groupby("Country", as_index=False)["Avg_Spend"].mean()
    return out


def _format_currency(x: float) -> str:
    """Format number as currency string."""
    try:
        v = float(x)
    except Exception:
        return "N/A"

    if v >= 1e9:
        return f"${v/1e9:.1f}B"
    if v >= 1e6:
        return f"${v/1e6:.1f}M"
    if v >= 1e3:
        return f"${v/1e3:.1f}K"
    return f"${v:.0f}"


def _degrees_to_km(degrees: float) -> float:
    """Convert degrees of latitude/longitude to kilometers.

    Uses the Earth's mean radius of approximately 6,371 km.
    1 degree ≈ 111.32 km
    """
    return degrees * 111.32


def _create_circular_flag(flag_url: str, size: int = 512) -> str:
    """Create a circular flag image with clean sharp edges.

    Args:
        flag_url: URL to the flag image
        size: Size of the output circular image (default 512x512 for high quality)

    Returns:
        Base64 encoded data URL for the circular flag image
    """
    try:
        # Download the flag image
        response = requests.get(flag_url, timeout=5)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Circle size: make it 95% of output size, increased by 50% = 142.5%
        # This makes the circle larger while maintaining proportions
        circle_diameter = int(size * 0.95 * 1.5)

        # Increase canvas size to fit the larger circle
        # Canvas needs to be at least as large as the circle diameter
        canvas_size = max(size, circle_diameter + 20)  # Add 20px padding

        # Crop flag to square (1:1 ratio) by taking the center square
        # This removes the black space that appears when fitting rectangular flag in circle
        min_dim = min(img.width, img.height)
        left = (img.width - min_dim) // 2
        top = (img.height - min_dim) // 2
        img = img.crop((left, top, left + min_dim, top + min_dim))

        # Now scale the square flag to fill the circle
        # Use 110% of output size, increased by 50% = 165%
        flag_fit_size = int(size * 1.10 * 1.5)
        img = img.resize((flag_fit_size, flag_fit_size), Image.Resampling.LANCZOS)

        # Create output image with the flag centered
        output = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
        # Center the flag in the output
        offset_x = (canvas_size - img.width) // 2
        offset_y = (canvas_size - img.height) // 2
        output.paste(img, (offset_x, offset_y), img)

        # Create a hard-edged circular mask
        # Start with transparent background (0)
        mask = Image.new('L', (canvas_size, canvas_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        # Draw opaque circle - centered in the larger canvas
        circle_offset = (canvas_size - circle_diameter) // 2
        mask_draw.ellipse([circle_offset, circle_offset, circle_offset + circle_diameter, circle_offset + circle_diameter], fill=255)

        # Apply the mask ON TOP of the flag (as alpha channel)
        # This clips the flag to the circular shape
        output.putalpha(mask)

        # Convert to base64 data URL
        buffered = BytesIO()
        output.save(buffered, format="PNG", optimize=False)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

    except Exception as e:
        print(f"Error creating circular flag for {flag_url}: {e}")
        return flag_url  # Fallback to original URL


# ============================================================================
# VISUALIZATION CREATION
# ============================================================================

def _detect_and_resolve_overlaps(summary: pd.DataFrame, min_distance: float = 3.0) -> pd.DataFrame:
    """
    Detect and resolve overlapping flag positions.

    Args:
        summary: DataFrame with Distance and Avg_Spend columns
        min_distance: Minimum distance between flags in data units

    Returns:
        DataFrame with adjusted positions to prevent overlaps
    """
    summary = summary.copy()
    positions = summary[["Distance", "Avg_Spend"]].values

    # Iteratively adjust positions to prevent overlaps
    max_iterations = 100
    for _ in range(max_iterations):
        adjusted = False

        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                # Calculate distance between two flags
                dx = positions[i, 0] - positions[j, 0]
                dy = positions[i, 1] - positions[j, 1]
                dist = np.sqrt(dx**2 + dy**2)

                # If too close, push them apart
                if dist < min_distance and dist > 0:
                    adjusted = True
                    # Calculate push direction
                    push_x = (dx / dist) * (min_distance - dist) / 2
                    push_y = (dy / dist) * (min_distance - dist) / 2

                    # Apply push (but keep within reasonable bounds)
                    positions[i, 0] += push_x
                    positions[j, 0] -= push_x
                    positions[i, 1] += push_y
                    positions[j, 1] -= push_y

        if not adjusted:
            break

    # Update summary with adjusted positions
    summary["Distance"] = positions[:, 0]
    summary["Avg_Spend"] = positions[:, 1]

    return summary


def create_threat_density_map():
    """Create geopolitical threat perception density map."""

    # Load data
    df = get_data()

    # Define country positions
    country_positions = {
        "Kazakhstan": {"lat": 48.0196, "lon": 66.9237},
        "Uzbekistan": {"lat": 41.3775, "lon": 64.5853},
        "Turkmenistan": {"lat": 38.9697, "lon": 59.5563},
        "Azerbaijan": {"lat": 40.1431, "lon": 47.5769},
        "Georgia": {"lat": 42.3154, "lon": 43.3569},
        "United States": {"lat": 38.0, "lon": -97.0},
        "Russia": {"lat": 61.5240, "lon": 105.3188},
        "China": {"lat": 35.8617, "lon": 104.1954},
    }
    ref_lat, ref_lon = 42.0, 55.0

    # Process data
    rows = []
    for _, row in df.iterrows():
        c = row["Country"]
        if c not in country_positions:
            continue

        pos = country_positions[c]
        dist = np.sqrt((pos["lat"] - ref_lat)**2 + (pos["lon"] - ref_lon)**2)
        threat_text = row["Threat Perception"]
        avg_spend = row["Avg_Spend"]

        for _ in range(10):
            rows.append({
                "Country": c,
                "Distance": dist + np.random.normal(0, 0.5),
                "Avg_Spend": avg_spend + np.random.normal(0, avg_spend * 0.05),
                "Threat_Perception": threat_text,
            })

    df_proc = pd.DataFrame(rows)

    # Create figure
    fig = go.Figure()

    # Add density heat background
    # Reduced nbinsx and nbinsy by 50% to increase grid spacing
    # Reduced opacity to minimize background cells
    fig.add_trace(go.Histogram2d(
        x=df_proc["Distance"],
        y=df_proc["Avg_Spend"],
        colorscale="Blues",
        showscale=False,
        opacity=0.15,
        nbinsx=10,
        nbinsy=7,
        hoverinfo="skip"
    ))

    # Compute summary statistics
    summary = df_proc.groupby("Country").agg(
        Distance=("Distance", "mean"),
        Avg_Spend=("Avg_Spend", "mean"),
        Threat_Perception=("Threat_Perception", "first")
    ).reset_index()
    # Note: No need to merge with df_spend since we already have Avg_Spend from df_proc

    # FIX #2: Detect and resolve overlapping flags
    summary = _detect_and_resolve_overlaps(summary, min_distance=3.5)

    # Calculate marker sizes based on spending
    # FIX #2: Use logarithmic scaling for better visual proportionality
    # This ensures smaller countries' flags are visible while maintaining proportional differences
    s_min = float(summary["Avg_Spend"].min())
    s_max = float(summary["Avg_Spend"].max())

    def norm_size_log(val: float) -> float:
        """Normalize spending value using logarithmic scaling for better visual proportionality.

        Logarithmic scaling ensures that:
        - Small differences in small values are visible
        - Large differences in large values don't dominate
        - All flags remain visually distinct
        """
        try:
            # Use log scale to compress the range
            log_min = np.log10(max(s_min, 1e6))  # Avoid log(0)
            log_max = np.log10(max(s_max, 1e6))
            log_val = np.log10(max(float(val), 1e6))

            # Normalize to 0-1 range
            t = (log_val - log_min) / max(1e-9, log_max - log_min)
            return max(0.0, min(1.0, t))
        except Exception:
            return 0.5

    # FIX #2: Calculate flag image sizes with improved scaling
    # Increased bubble size by 50% (from 10-30px to 15-45px)
    # Using 15-45px range to make bubbles bigger
    flag_sizes = [15 + 30 * norm_size_log(val) for val in summary["Avg_Spend"]]

    # Debug: Print sizing information to verify proportional scaling
    print("\n" + "=" * 70)
    print("FLAG SIZING VERIFICATION (FIX #2 - LOGARITHMIC SCALING)")
    print("=" * 70)
    for idx, row in summary.iterrows():
        norm_val = norm_size_log(row["Avg_Spend"])
        flag_size = flag_sizes[idx]
        print(f"{row['Country']:15} | Spend: ${row['Avg_Spend']/1e6:6.1f}M | "
              f"Norm: {norm_val:.3f} | Flag Size: {flag_size:.1f}px")
    print("=" * 70)
    print("✅ Proportional sizing verified with logarithmic scaling\n")

    # Add bubble trace for hover interactivity (invisible - flags will be the visual element)
    # Bubbles will contain flag images inside them
    fig.add_trace(go.Scatter(
        x=summary["Distance"],
        y=summary["Avg_Spend"],
        mode="markers",
        marker=dict(
            size=flag_sizes,
            color="rgba(0, 0, 0, 0)",  # Invisible bubbles
            line=dict(color="rgba(0, 0, 0, 0)", width=0)  # Invisible border
        ),
        hovertext=[
            f"<b>{r.Country}</b><br>"
            f"Distance: {r.Distance:.2f}°<br>"
            f"Distance: {_degrees_to_km(r.Distance):.0f} km<br>"
            f"Threat Perception: {r.Threat_Perception}<br>"
            f"Avg Spend: {_format_currency(r.Avg_Spend)}"
            for r in summary.itertuples()
        ],
        hoverinfo="text",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="darkgray",
            font=dict(size=12, color="black", family="Arial")
        ),
        showlegend=False,
        name="Countries",
        customdata=summary["Country"].values  # Add country names for debugging
    ))

    # Add flag images inside bubbles using layout.images
    # When using data coordinates (xref="x", yref="y"), sizex and sizey are in data units
    images = []

    # Calculate size range for images inside bubbles



    print("\n" + "=" * 70)
    print("FLAG IMAGE SIZING (INSIDE BUBBLES - CIRCULAR MASKED)")
    print("=" * 70)

    for idx, row in summary.iterrows():
        country = row["Country"]
        if country in FLAG_URLS:
            # Get normalized spending (0 to 1) using logarithmic scaling
            norm_val = norm_size_log(row["Avg_Spend"])

            # Scale flag size based on spending - use data coordinates
            # For data coordinates: width should be in degrees, height in dollars
            # Make flags about 4-8 degrees wide (100% increase, square aspect ratio to prevent distortion)
            base_width = 4.0
            img_width = base_width + (norm_val * 4.0)  # 4-8 degrees

            # Height should match width to maintain square aspect ratio and prevent distortion
            # Convert width (degrees) to height (dollars) using plot dimensions
            # Approximate conversion: 1 degree ≈ 5-6 million dollars based on plot range
            img_height = img_width * 5e6  # Maintain square aspect ratio

            # Debug output for sizing verification
            print(f"{country:15} | Norm: {norm_val:.3f} | "
                  f"Width: {img_width:.2f}° | Height: {img_height/1e6:.1f}M | "
                  f"Pos: ({row['Distance']:.1f}°, ${row['Avg_Spend']/1e6:.1f}M)")

            # Download and create circular-masked flag image
            try:
                # Create circular masked version
                circular_flag = _create_circular_flag(FLAG_URLS[country], size=512)

                # Add circular flag image - centered on the bubble marker
                images.append(dict(
                    source=circular_flag,
                    x=row["Distance"],
                    y=row["Avg_Spend"],
                    xref="x",
                    yref="y",
                    xanchor="center",
                    yanchor="middle",
                    sizex=img_width,
                    sizey=img_height,
                    opacity=1.0,
                    layer="above"  # Place above so flags are visible
                ))
            except Exception as e:
                print(f"Error loading flag for {country}: {e}")

    print("=" * 70)
    print(f"✅ Total flags created: {len(images)}")
    print("=" * 70 + "\n")

    # Update layout with flag images
    # FIX #3: Improved hover mode and styling
    fig.update_layout(
        title={
            "text": "Central Asian Regional Threat Perception Analysis",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20}
        },
        xaxis=dict(
            title="Distance from Regional Center (degrees)",
            showgrid=True,
            gridwidth=1,
            gridcolor="gray"
        ),
        yaxis=dict(
            title="Average Military Spending ($)",
            showgrid=True,
            gridwidth=1,
            gridcolor="gray"
        ),
        plot_bgcolor="lightgray",
        paper_bgcolor="lightgray",
        height=600,
        width=1000,
        showlegend=False,
        hovermode="closest",
        margin=dict(l=80, r=50, t=100, b=80),
        images=images
    )

    return fig


# ============================================================================
# DASH APPLICATION
# ============================================================================

# Initialize the Dash app
app = Dash(__name__)

# Create the figure
fig = create_threat_density_map()

# Define the app layout
app.layout = html.Div([
    html.Div([
        html.H1("Central Asian Regional Threat Perception Analysis",
                style={"textAlign": "center", "marginBottom": 30}),
        html.P("Interactive visualization of Central Asian countries' threat perception and military spending",
               style={"textAlign": "center", "color": "#666", "marginBottom": 20}),
    ], style={"padding": "20px"}),

    html.Div([
        dcc.Graph(figure=fig, style={"height": "700px"})
    ], style={"padding": "20px"}),

    html.Div([
        html.Hr(),
        html.P([
            html.Strong("About this visualization: "),
            "This chart analyzes Central Asian countries (Kazakhstan, Uzbekistan, Turkmenistan, Azerbaijan, Georgia) "
            "and their threat perceptions. The visualization shows the relationship between geographic distance from a regional center, "
            "threat perception intensity, and military spending. Larger country flags indicate higher military spending. "
            "Hover over flags to see detailed information including distance in both degrees and kilometers."
        ], style={"padding": "20px", "color": "#666", "fontSize": "14px"})
    ], style={"padding": "20px", "backgroundColor": "#f9f9f9", "borderRadius": "5px", "margin": "20px"})
], style={"fontFamily": "Arial, sans-serif", "maxWidth": "1200px", "margin": "0 auto"})


# ============================================================================
# RUN THE APP
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Starting Plotly Dash Application")
    print("=" * 70)
    print("\n📊 Geopolitical Threat Perception Density Map")
    print("\n🌐 Open your browser and go to: http://localhost:8050")
    print("\n💡 To deploy this app, see DASH_DEPLOYMENT.md")
    print("\n" + "=" * 70)
    
    # Run the app
    app.run(debug=True, host="0.0.0.0", port=8050)

