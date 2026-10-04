import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Extreme Event Warning System", layout="wide")

st.title("Extreme Event Early Warning System")
st.markdown("AI-Powered Early Warning System for Heatwaves & Droughts (7-day ahead predictions)")

# ── Load data ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df_preds = pd.read_csv(os.path.join(base_dir, 'results', 'extreme_event_warnings.csv'))
    df_preds['DATE'] = pd.to_datetime(df_preds['DATE'])
    df_preds['Prediction_Date'] = pd.to_datetime(df_preds['Prediction_Date'])

    df_actuals = pd.read_csv(os.path.join(base_dir, 'data', 'processed', 'event_labeled_dataset.csv'))
    df_actuals['DATE'] = pd.to_datetime(df_actuals['DATE'])

    return df_preds, df_actuals

with st.spinner("Loading climate data..."):
    df_preds, df_actuals = load_data()

# ── Sidebar controls ─────────────────────────────────────────────────────────
st.sidebar.header("Controls")

cities = sorted(df_preds['LOCATION'].unique())
selected_city = st.sidebar.selectbox("Select City", cities)

# Filter by city
city_preds   = df_preds[df_preds['LOCATION'] == selected_city].sort_values('DATE')
city_actuals = df_actuals[df_actuals['LOCATION'] == selected_city].sort_values('DATE')

# Date selection using separate Year / Month / Day dropdowns
available_years = sorted(city_preds['DATE'].dt.year.unique(), reverse=True)
default_year = available_years[0]
selected_year = st.sidebar.selectbox("Year", available_years, index=0)

months_in_year = sorted(city_preds[city_preds['DATE'].dt.year == selected_year]['DATE'].dt.month.unique())
month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
month_options = [f"{m} - {month_names[m]}" for m in months_in_year]
selected_month_str = st.sidebar.selectbox("Month", month_options, index=len(month_options)-1)
selected_month = int(selected_month_str.split(" - ")[0])

days_in_month = sorted(city_preds[(city_preds['DATE'].dt.year == selected_year) & (city_preds['DATE'].dt.month == selected_month)]['DATE'].dt.day.unique())
selected_day = st.sidebar.selectbox("Day", days_in_month, index=0)

selected_date = pd.to_datetime(f"{selected_year}-{selected_month:02d}-{selected_day:02d}")

# Find the closest available date in the dataset
closest_idx = (city_preds['DATE'] - selected_date).abs().idxmin()
current_pred = city_preds.loc[closest_idx]
actual_date = current_pred['DATE']

# ── 7-Day Forecast boxes ─────────────────────────────────────────────────────
st.header(f"7-Day Forecast for {selected_city}")
st.markdown(
    f"**As of:** {actual_date.strftime('%d %b %Y')}  →  "
    f"**Predicting for:** {current_pred['Prediction_Date'].strftime('%d %b %Y')}"
)

# Helper to render the box in the correct color based on risk level
def render_risk_box(event_name, warning_level, probability):
    # Normalize the warning text for display
    if warning_level == "COMPOUND EVENT WARNING":
        display_level = "HIGH RISK"
    else:
        display_level = warning_level

    content = f"**{event_name}**\n\nStatus: **{display_level}**\n\nProbability: {probability:.0%}"
    if "HIGH" in display_level:
        st.error(content)
    elif "MEDIUM" in display_level:
        st.warning(content)
    else:
        st.success(content)

col1, col2, col3 = st.columns(3)

with col1:
    render_risk_box("Heatwave", current_pred['Heatwave_Warning'], current_pred['Heatwave_Probability'])

with col2:
    render_risk_box("Drought", current_pred['Drought_Warning'], current_pred['Drought_Probability'])

with col3:
    render_risk_box("Compound Event", current_pred['Compound_Warning'], current_pred['Compound_Probability'])

st.divider()

# ── Actual vs Predicted Graph ────────────────────────────────────────────────
st.header("Actual vs Predicted — Model Verification")
st.markdown(
    "The grey line shows actual daily max temperature. "
    "**Red dots** = heatwave actually occurred. "
    "**Blue circles** = model predicted it 7 days earlier. "
    "Overlapping dots = accurate prediction."
)

start_date = actual_date - pd.Timedelta(days=90)
end_date   = actual_date + pd.Timedelta(days=7)

recent_actuals = city_actuals[
    (city_actuals['DATE'] >= start_date) & (city_actuals['DATE'] <= end_date)
].copy()

recent_preds = city_preds[
    (city_preds['Prediction_Date'] >= start_date) & (city_preds['Prediction_Date'] <= end_date)
].copy()

fig = go.Figure()

# Actual temperature line
fig.add_trace(go.Scatter(
    x=recent_actuals['DATE'],
    y=recent_actuals['TMAX'],
    mode='lines',
    name='Actual Max Temp (°C)',
    line=dict(color='#888888', width=1.5),
))

# Actual heatwave days (red dots)
actual_hw = recent_actuals[recent_actuals['heatwave_day'] == 1]
fig.add_trace(go.Scatter(
    x=actual_hw['DATE'],
    y=actual_hw['TMAX'],
    mode='markers',
    name='Actual Heatwave',
    marker=dict(color='red', size=10),
))

# Predicted heatwave days (blue open circles)
predicted_hw = recent_preds[recent_preds['Heatwave_Warning'] == 'HIGH RISK'][['Prediction_Date']].copy()

# Merge with actuals to get the actual temperature on the predicted date
pred_with_temp = predicted_hw.merge(
    recent_actuals[['DATE', 'TMAX']].rename(columns={'TMAX': 'actual_TMAX'}),
    left_on='Prediction_Date',
    right_on='DATE',
    how='inner'
)

if not pred_with_temp.empty:
    fig.add_trace(go.Scatter(
        x=pred_with_temp['Prediction_Date'],
        y=pred_with_temp['actual_TMAX'],
        mode='markers',
        name='Predicted Heatwave (7-day ahead)',
        marker=dict(color='royalblue', size=16, symbol='circle-open', line=dict(width=2.5)),
    ))

fig.update_layout(
    title=f"Heatwave: Actual vs Predicted in {selected_city} (Model Performance Over 90 Days)",
    xaxis_title="Date",
    yaxis_title="Max Temperature (°C)",
    xaxis=dict(
        tickformat="%d %b\n%Y",
        dtick="M1",
    ),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(t=80),
)

st.plotly_chart(fig, use_container_width=True)
