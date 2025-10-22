# 🌍 Geopolitical Analysis Dashboard

A multi-page interactive dashboard analyzing Central Asian regional threat perception and defense systems using Plotly visualizations.

## 🌐 Live Dashboard

**Visit the dashboard:** https://akfave99.github.io/Data_Dashboards/

## 📊 Dashboard Pages

### Home Page
Beautiful landing page with all available charts displayed as interactive cards.

### Chart Pages
1. **Threat Perception** - Central Asian Regional Threat Perception Analysis (3D density map with flag images)
2. **Supplier Influence** - Defense Supplier Influence 3D Surface
3. **Defense Systems** - Defense Systems Analysis (Polar/Radar chart)
4. **Multi-Country Radar** - Multi-Country Radar Comparison
5. **Priorities Heatmap** - Defense Priorities Heatmap
6. **Supplier Connections** - Supplier Connections Sankey Diagram

## 🎨 Features

- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Dark Theme** - Professional dark blue color scheme
- ✅ **Interactive Charts** - Zoom, pan, rotate, and download as PNG
- ✅ **Navigation Bar** - Quick access to all charts with mobile menu
- ✅ **Beautiful Styling** - Gradient backgrounds, smooth transitions, hover effects

## 📁 Project Structure

```
Data_Dashboards/
├── docs/                                    # GitHub Pages source
│   ├── index.html                          # Home page
│   ├── chart0.html through chart5.html      # Individual chart pages
│   ├── chart*.html                         # Raw Plotly chart data
│   └── .nojekyll                           # GitHub Pages config
├── geopolitical-dashboard/                 # Source code
│   ├── Transcaspian_Defense_Data_app.py    # Main Dash app
│   ├── geopolitical_app.py                 # Chart generation functions
│   ├── chart_data.py                       # Data module
│   ├── pages/                              # Dash page components
│   ├── generate_all_charts.py              # Generate all charts as HTML
│   ├── create_dashboard_html.py            # Create multi-page dashboard
│   ├── upload_charts_to_plotly.py          # Upload to Plotly Cloud
│   ├── requirements.txt                    # Python dependencies
│   ├── Procfile                            # Deployment config
│   └── .env                                # API credentials (not committed)
├── .github/workflows/
│   └── deploy-pages.yml                    # GitHub Actions deployment
└── README.md                               # This file
```

## 🚀 Deployment

The dashboard is automatically deployed to GitHub Pages via GitHub Actions whenever changes are pushed to the `main` branch.

### GitHub Pages Configuration
- **Source:** `/docs` folder
- **Branch:** `main`
- **URL:** https://akfave99.github.io/Data_Dashboards/
- **Workflow:** `.github/workflows/deploy-pages.yml`

## 🔧 Local Development

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. Clone the repository:
```bash
git clone https://github.com/akfave99/Data_Dashboards.git
cd Data_Dashboards
```

2. Install dependencies:
```bash
cd geopolitical-dashboard
pip install -r requirements.txt
```

3. Generate charts:
```bash
python generate_all_charts.py
python create_dashboard_html.py
```

4. Copy to docs folder:
```bash
cp *.html ../docs/
```

5. Commit and push:
```bash
cd ..
git add docs/
git commit -m "Update dashboard"
git push origin main
```

## 📊 Updating the Dashboard

To update the dashboard:

1. Modify chart generation code in `geopolitical-dashboard/`
2. Run `python generate_all_charts.py` to generate new charts
3. Run `python create_dashboard_html.py` to create dashboard pages
4. Copy HTML files to `/docs` folder
5. Commit and push to GitHub
6. GitHub Actions will automatically deploy the changes

## 🔐 Security

- API credentials are stored in `.env` file (not committed)
- `.env` is in `.gitignore` to prevent accidental commits
- All sensitive data is kept local

## 📝 Technologies Used

- **Plotly** - Interactive visualizations
- **Bootstrap 5** - Responsive UI framework
- **GitHub Pages** - Static site hosting
- **GitHub Actions** - Automated deployment
- **Python** - Data processing and chart generation

## 👤 Author

Created by: A.K. Faver

## 📄 License

This project is open source and available under the MIT License.

---

**Dashboard URL:** https://akfave99.github.io/Data_Dashboards/
