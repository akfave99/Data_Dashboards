# Geopolitical Analysis Dashboard

A comprehensive interactive dashboard for analyzing geopolitical threat perception and defense supplier influence across Central Asian countries and the Caucasus region.

## 📊 Features

- **8 Interactive Charts** with real-time data visualization
- **Multi-page Application** built with Plotly Dash
- **Responsive Design** that works on all devices
- **Dark Theme** with professional Bootstrap styling
- **Interactive Controls** including dropdowns, toggles, and filters
- **Production-Ready** configuration for cloud deployment

## 🎯 Charts Included

1. **Threat Perception Map** - Geopolitical threat density visualization
2. **Supplier Influence Surface** - 3D surface showing defense supplier influence patterns
3. **Regional Influence Map** - Geographic choropleth of supplier influence by region
4. **Defense Systems Analysis** - 3D scatter plot of defense systems by supplier
5. **Multi-Country Radar** - Radar chart comparing influence metrics across countries
6. **Priorities Heatmap** - Correlation heatmap of defense priorities and suppliers
7. **Regional Density Map** - Scatter plot showing regional distribution of defense metrics
8. **Supplier Connections** - Sankey diagram visualizing supplier-receiver relationships

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip or conda

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/geopolitical-dashboard.git
cd geopolitical-dashboard
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:8050
```

## 📁 Project Structure

```
geopolitical-dashboard/
├── app.py                    # Main Dash application
├── chart_data.py            # Mock data module
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment configuration
├── runtime.txt             # Python version specification
├── README.md               # This file
├── .gitignore              # Git ignore rules
├── pages/                  # Multi-page app pages
│   ├── __init__.py
│   ├── home.py            # Threat Perception page
│   ├── chart1.py          # Supplier Influence Surface
│   ├── chart2.py          # Regional Influence Map
│   ├── chart3.py          # Defense Systems Analysis
│   ├── chart4.py          # Multi-Country Radar
│   ├── chart5.py          # Priorities Heatmap
│   ├── chart6.py          # Regional Density Map
│   └── chart7.py          # Supplier Connections
└── assets/                # Static files
    └── custom.css         # Custom styling
```

## 🛠️ Technology Stack

- **Plotly Dash** - Web application framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Dash Bootstrap Components** - UI components
- **Gunicorn** - Production server

## 📦 Dependencies

See `requirements.txt` for complete list:
- plotly>=5.17.0
- dash>=2.14.0
- dash-bootstrap-components>=1.4.0
- pandas>=2.0.0
- numpy>=1.24.0
- gunicorn>=21.2.0

## �� Deployment

### Deploy to Plotly Cloud

1. Push to GitHub:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. Go to https://chart-studio.plotly.com/
3. Click "Create" → "Deploy App"
4. Select "Dash App" and connect your GitHub repository
5. Select the branch and deploy

### Deploy to Heroku

1. Install Heroku CLI:
```bash
brew install heroku
```

2. Login and create app:
```bash
heroku login
heroku create your-app-name
```

3. Deploy:
```bash
git push heroku main
```

Your app will be available at: `https://your-app-name.herokuapp.com`

## 📝 Configuration

### Environment Variables

If needed, create a `.env` file:
```
DEBUG=False
PORT=8050
```

### Customization

- **Styling**: Edit `assets/custom.css`
- **Data**: Modify `chart_data.py`
- **Charts**: Edit individual files in `pages/`

## 🔧 Development

### Running in Development Mode

```bash
python app.py
```

The app will run with debug mode enabled at `http://localhost:8050`

### Making Changes

1. Edit the relevant files
2. The app will auto-reload (if debug mode is on)
3. Test your changes in the browser

## 📊 Data

The dashboard uses mock data defined in `chart_data.py`. To use real data:

1. Replace the `get_data()` function in `chart_data.py`
2. Ensure your data has the required columns
3. Update chart files as needed

## 🐛 Troubleshooting

### App won't start
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.11+
- Check for port conflicts on port 8050

### Charts not loading
- Verify `pages/` directory structure
- Check that `pages/__init__.py` exists
- Review browser console for errors

### Styling issues
- Clear browser cache
- Verify `assets/custom.css` is present
- Check CSS file syntax

## 📞 Support

- **Plotly Dash Documentation**: https://plotly.com/dash/
- **Plotly Community**: https://community.plotly.com/
- **GitHub Issues**: Create an issue in this repository

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Created by:** A.K. Faver  
**Date:** October 21, 2025

## 🙏 Acknowledgments

- Built with [Plotly Dash](https://plotly.com/dash/)
- Styled with [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- Inspired by geopolitical analysis best practices

---

**Ready to deploy? Follow the deployment instructions above!** 🚀
