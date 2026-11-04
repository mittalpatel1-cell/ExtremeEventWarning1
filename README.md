# Extreme Event Warning System

## Project Overview
An early warning system that analyzes climate data to monitor heatwaves, droughts, and compound extreme events across 12 Indian locations.

The project uses historical climate data from NASA POWER, IMD, and NOAA ONI. Machine learning models generate event predictions, while anomaly detection identifies unusual climate patterns.

## Live Dashboard & Deployment
- **Live Application**: [https://pbl-project.streamlit.app](https://pbl-project.streamlit.app)
- **Streamlit Badge**: [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pbl-project.streamlit.app)

## Project Documentation
- **Presentation Slides**: [docs/PBL_Presentation.pptx](docs/PBL_Presentation.pptx)

## Main Features
- Climate data processing and integration
- Heatwave, drought, and compound event labeling
- Random Forest, Decision Tree, and SVM model comparison
- Seven-day-ahead event prediction
- Multivariate and 30-day anomaly analysis
- Streamlit dashboard

## Project Structure
- `src/` - Data processing, model training, prediction, and dashboard scripts
- `data/raw/` - Raw climate datasets
- `data/processed/` - Prepared datasets
- `results/` - Trained models, predictions, and evaluation results
- `archive/` - Older testing and validation scripts
- `requirements.txt` - Python dependencies

## Setup
Activate the virtual environment, then install dependencies if needed:

```bash
pip install -r requirements.txt
```

## Run the Dashboard Locally
From the project root, run:

```bash
streamlit run src/dashboard.py
```

## Important Notes
- Event labels use project-defined thresholds and are not official IMD declarations.
- Predictions depend on trained model files stored in `results/`.
- Keep the existing environment and model files intact when sharing the project.
