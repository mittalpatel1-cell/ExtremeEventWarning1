
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


ROOT = Path(__file__).resolve().parents[1]

FORECAST_PATH = ROOT / "results" / "extreme_event_warnings.csv"
COMPARISON_PATH = ROOT / "results" / "model_comparison.csv"
ACTUAL_PATH = ROOT / "data" / "processed" / "event_labeled_dataset.csv"


st.set_page_config(
    page_title="Extreme Event Warning System",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# UI THEME
# --------------------------------------------------

st.markdown("""
<style>
    :root {
        --navy: #24364B;
        --steel: #344E70;
        --blue: #54799F;
        --red: #9B493C;
        --green: #466B5D;
        --gold: #A87935;
        --white: #FFFFFF;
        --background: #F5F7FA;
        --surface: #FFFFFF;
        --border: #DCE3EB;
        --muted: #657386;
        --text: #24364B;
    }

    .stApp {
        background-color: var(--background);
        color: var(--text);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1500px;
    }

    h1, h2, h3, h4 {
        color: var(--navy) !important;
        font-weight: 700 !important;
        letter-spacing: -0.35px;
    }

    h1 {
        font-size: 2.15rem !important;
    }

    h2 {
        font-size: 1.55rem !important;
    }

    h3 {
        font-size: 1.15rem !important;
    }

    p, label {
        color: var(--text);
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    .subtitle {
        color: var(--muted);
        font-size: 15px;
        line-height: 1.7;
        margin-top: -4px;
        margin-bottom: 24px;
    }

    .section-label {
        color: var(--steel);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #FFFFFF;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--navy) !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--muted);
    }

    [data-testid="stSidebar"] hr {
        border-color: var(--border);
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border-color: #CBD5E1;
        border-radius: 9px;
    }

    div[data-baseweb="select"] span {
        color: var(--navy);
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--steel);
        box-shadow: 0 0 0 1px var(--steel);
    }

    .forecast-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 13px;
        padding: 22px;
        min-height: 174px;
        box-shadow: 0 3px 12px rgba(36, 54, 75, 0.045);
    }

    .forecast-name {
        color: var(--muted);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.2px;
    }

    .forecast-status {
        color: var(--navy);
        font-size: 23px;
        font-weight: 750;
        margin-top: 17px;
        margin-bottom: 7px;
    }

    .forecast-probability {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 15px;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 17px 18px;
        box-shadow: 0 3px 12px rgba(36, 54, 75, 0.035);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    div[data-testid="stMetricValue"] {
        color: var(--navy);
        font-weight: 750;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
        background: #FFFFFF;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    .stButton button {
        background: var(--navy);
        color: #FFFFFF;
        border: 1px solid var(--navy);
        border-radius: 8px;
    }

    .stButton button:hover {
        background: var(--steel);
        color: #FFFFFF;
        border-color: var(--steel);
    }

    hr {
        border-color: var(--border);
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .dashboard-footer {
        text-align: center;
        color: #718096;
        font-size: 12px;
        line-height: 1.8;
        padding: 14px 8px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def load_csv(path):
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception as exc:
        st.warning(f"Could not read {path.name}: {exc}")
        return pd.DataFrame()


def prepare_dates(df, columns):
    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column], errors="coerce"
            )

    return df


def find_column(df, names):
    for name in names:
        if name in df.columns:
            return name
    return None


def probability_percent(value):
    if pd.isna(value):
        return None

    try:
        value = float(value)
    except (TypeError, ValueError):
        return None

    if 0 <= value <= 1:
        value *= 100

    return max(0, min(value, 100))


def get_probability(row, column):
    if column not in row.index:
        return None
    return probability_percent(row[column])


def warning_value(value):
    if pd.isna(value):
        return False

    if isinstance(value, str):
        normalised = value.strip().upper()

        return normalised in {
            "1", "1.0", "TRUE", "YES", "WARNING", "HIGH",
            "HIGH RISK", "POSITIVE", "HEATWAVE",
            "HEATWAVE WARNING"
        }

    try:
        return bool(value)
    except (TypeError, ValueError):
        return False


def get_warning(row, column):
    if column not in row.index:
        return False

    return warning_value(row[column])


def get_status(warning, probability):
    if warning:
        return "Warning"
    if probability is not None and probability >= 50:
        return "Elevated Risk"
    if probability is not None and probability >= 25:
        return "Moderate Risk"
    return "Low Risk"


def render_forecast_card(title, warning, probability):
    status = get_status(warning, probability)

    if status == "Warning":
        accent = "#9B493C"
    elif status == "Elevated Risk":
        accent = "#A87935"
    elif status == "Moderate Risk":
        accent = "#54799F"
    else:
        accent = "#466B5D"

    probability_text = (
        f"{probability:.1f}% predicted probability"
        if probability is not None
        else "Probability unavailable"
    )

    bar_width = probability if probability is not None else 0

    st.markdown(
        f"""
        <div class="forecast-card"
             style="border-top: 4px solid {accent};">
            <div class="forecast-name">{title}</div>
            <div class="forecast-status">{status}</div>
            <div class="forecast-probability">{probability_text}</div>
            <div style="background:#E8EDF3;height:6px;border-radius:6px;">
                <div style="background:{accent};width:{bar_width:.1f}%;
                            height:6px;border-radius:6px;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

forecast_df = load_csv(FORECAST_PATH)
actual_df = load_csv(ACTUAL_PATH)
comparison_df = load_csv(COMPARISON_PATH)

if not forecast_df.empty:
    forecast_df = prepare_dates(
        forecast_df, ["DATE", "Prediction_Date"]
    )

if not actual_df.empty:
    actual_df = prepare_dates(actual_df, ["DATE"])


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="section-label">CLIMATE INTELLIGENCE / MONITORING</div>',
    unsafe_allow_html=True
)

st.title("Extreme Event Warning System")

st.markdown(
    '<div class="subtitle">'
    'Monitor heatwaves, droughts and compound extreme events '
    'using historical climate data and machine learning predictions.'
    '</div>',
    unsafe_allow_html=True
)

if forecast_df.empty and actual_df.empty:
    st.error(
        "No forecast or historical data could be loaded. "
        "Check your CSV paths."
    )
    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.markdown("## Dashboard Filters")
st.sidebar.caption("Choose a location and date to explore climate conditions.")

location_values = []

if not forecast_df.empty and "LOCATION" in forecast_df.columns:
    location_values.extend(
        forecast_df["LOCATION"].dropna().astype(str).tolist()
    )

if not actual_df.empty and "LOCATION" in actual_df.columns:
    location_values.extend(
        actual_df["LOCATION"].dropna().astype(str).tolist()
    )

locations = sorted(set(location_values))

if not locations:
    st.error("No locations were found in the available data.")
    st.stop()

selected_location = st.sidebar.selectbox("Location", locations)

date_values = []

if not forecast_df.empty and "LOCATION" in forecast_df.columns:
    location_forecasts = forecast_df[
        forecast_df["LOCATION"].astype(str) == selected_location
    ]

    target_col = (
        "Prediction_Date"
        if "Prediction_Date" in location_forecasts.columns
        and location_forecasts["Prediction_Date"].notna().any()
        else "DATE"
    )

    if target_col in location_forecasts.columns:
        date_values.extend(
            location_forecasts[target_col].dropna().tolist()
        )

if not actual_df.empty and "LOCATION" in actual_df.columns:
    location_actuals = actual_df[
        actual_df["LOCATION"].astype(str) == selected_location
    ]

    if "DATE" in location_actuals.columns:
        date_values.extend(
            location_actuals["DATE"].dropna().tolist()
        )

if not date_values:
    st.error("No dates are available for this location.")
    st.stop()

date_series = pd.to_datetime(
    pd.Series(date_values), errors="coerce"
).dropna()

available_years = sorted(date_series.dt.year.unique().tolist())

if not available_years:
    st.error("No valid years were found.")
    st.stop()

selected_year = st.sidebar.selectbox(
    "Year",
    available_years,
    index=len(available_years) - 1
)

available_months = sorted(
    date_series[date_series.dt.year == selected_year]
    .dt.month.unique().tolist()
)

month_names = {
    1: "January", 2: "February", 3: "March",
    4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September",
    10: "October", 11: "November", 12: "December"
}

selected_month = st.sidebar.selectbox(
    "Month",
    available_months,
    format_func=lambda month: month_names[month],
    index=len(available_months) - 1
)

available_days = sorted(
    date_series[
        (date_series.dt.year == selected_year)
        & (date_series.dt.month == selected_month)
    ].dt.day.unique().tolist()
)

selected_day = st.sidebar.selectbox(
    "Day",
    available_days,
    index=len(available_days) - 1
)

selected_date = pd.Timestamp(
    year=int(selected_year),
    month=int(selected_month),
    day=int(selected_day)
)

st.sidebar.markdown("---")
st.sidebar.caption(
    f"Selected date: {selected_date.strftime('%d %B %Y')}"
)


# --------------------------------------------------
# FORECAST OVERVIEW
# --------------------------------------------------

location_forecasts = pd.DataFrame()

if not forecast_df.empty and "LOCATION" in forecast_df.columns:
    location_forecasts = forecast_df[
        forecast_df["LOCATION"].astype(str) == selected_location
    ].copy()

    target_col = (
        "Prediction_Date"
        if "Prediction_Date" in location_forecasts.columns
        and location_forecasts["Prediction_Date"].notna().any()
        else "DATE"
    )

    if target_col in location_forecasts.columns:
        location_forecasts = location_forecasts[
            location_forecasts[target_col].dt.normalize()
            == selected_date.normalize()
        ]

st.markdown("## Forecast Overview")
st.caption(
    f"{selected_location} · {selected_date.strftime('%d %B %Y')}"
)

if location_forecasts.empty:
    st.info("No forecast is available for the selected target date.")
else:
    row = location_forecasts.iloc[-1]

    col1, col2, col3 = st.columns(3)

    with col1:
        render_forecast_card(
            "HEATWAVE",
            get_warning(row, "Heatwave_Warning"),
            get_probability(row, "Heatwave_Probability")
        )

    with col2:
        render_forecast_card(
            "DROUGHT",
            get_warning(row, "Drought_Warning"),
            get_probability(row, "Drought_Probability")
        )

    with col3:
        render_forecast_card(
            "COMPOUND EVENT",
            get_warning(row, "Compound_Warning"),
            get_probability(row, "Compound_Probability")
        )


# --------------------------------------------------
# TEMPERATURE AND EVENT HISTORY
# --------------------------------------------------

st.markdown("---")
st.markdown("## Temperature & Event History")

st.caption(
    "Daily maximum temperature, observed heatwave days, "
    "and predicted heatwave events over the selected 30-day period."
)

if (
    not actual_df.empty
    and "TMAX" in actual_df.columns
    and "DATE" in actual_df.columns
    and "LOCATION" in actual_df.columns
):
    location_actuals = actual_df[
        actual_df["LOCATION"].astype(str) == selected_location
    ].copy()

    location_actuals = location_actuals.dropna(subset=["DATE"])
    location_actuals = location_actuals.sort_values("DATE")

    location_actuals["DATE"] = pd.to_datetime(
        location_actuals["DATE"], errors="coerce"
    ).dt.normalize()

    location_actuals["TMAX"] = pd.to_numeric(
        location_actuals["TMAX"], errors="coerce"
    )

    start_date = selected_date - pd.Timedelta(days=29)
    end_date = selected_date + pd.Timedelta(days=1)

    chart_actuals = location_actuals[
        (location_actuals["DATE"] >= start_date)
        & (location_actuals["DATE"] < end_date)
    ].copy()

    fig = go.Figure()

    if not chart_actuals.empty:
        fig.add_trace(
            go.Scatter(
                x=chart_actuals["DATE"],
                y=chart_actuals["TMAX"],
                mode="lines",
                name="Maximum Temperature",
                line=dict(color="#344E70", width=2.7),
                hovertemplate=(
                    "Date: %{x|%d %b %Y}<br>"
                    "Temperature: %{y:.1f} °C<extra></extra>"
                )
            )
        )

        heatwave_col = find_column(
            chart_actuals,
            ["heatwave_day", "Heatwave_Warning", "HEATWAVE"]
        )

        if heatwave_col:
            observed = chart_actuals[
                chart_actuals[heatwave_col].apply(warning_value)
            ]

            fig.add_trace(
                go.Scatter(
                    x=observed["DATE"],
                    y=observed["TMAX"],
                    mode="markers",
                    name="Observed Heatwave",
                    marker=dict(
                        color="#9B493C",
                        size=9,
                        symbol="circle",
                        line=dict(color="#FFFFFF", width=1.5)
                    ),
                    hovertemplate=(
                        "Observed heatwave<br>"
                        "Date: %{x|%d %b %Y}<br>"
                        "Temperature: %{y:.1f} °C<extra></extra>"
                    )
                )
            )

    # Predicted heatwave markers
    if (
        not forecast_df.empty
        and "Heatwave_Warning" in forecast_df.columns
        and "LOCATION" in forecast_df.columns
    ):
        chart_forecasts = forecast_df[
            forecast_df["LOCATION"].astype(str) == selected_location
        ].copy()

        target_col = (
            "Prediction_Date"
            if "Prediction_Date" in chart_forecasts.columns
            and chart_forecasts["Prediction_Date"].notna().any()
            else "DATE"
        )

        if target_col in chart_forecasts.columns:
            chart_forecasts[target_col] = pd.to_datetime(
                chart_forecasts[target_col], errors="coerce"
            ).dt.normalize()

            chart_forecasts = chart_forecasts.dropna(subset=[target_col])

            chart_forecasts = chart_forecasts[
                (chart_forecasts[target_col] >= start_date)
                & (chart_forecasts[target_col] < end_date)
            ].copy()

            predicted = chart_forecasts[
                chart_forecasts["Heatwave_Warning"].apply(warning_value)
            ].copy()

            if not predicted.empty:
                predicted["_Plot_Date"] = predicted[target_col]

                actual_temperatures = location_actuals[
                    ["DATE", "TMAX"]
                ].dropna(subset=["DATE", "TMAX"]).copy()

                actual_temperatures["_Plot_Date"] = pd.to_datetime(
                    actual_temperatures["DATE"], errors="coerce"
                ).dt.normalize()

                temperature_lookup = (
                    actual_temperatures
                    .drop_duplicates("_Plot_Date")
                    .set_index("_Plot_Date")["TMAX"]
                )

                predicted["_Actual_Temperature"] = (
                    predicted["_Plot_Date"].map(temperature_lookup)
                )

                observed_max = (
                    chart_actuals["TMAX"].max()
                    if not chart_actuals.empty
                    else float("nan")
                )

                fallback_temperature = (
                    float(observed_max) + 2
                    if pd.notna(observed_max)
                    else 40.0
                )

                predicted["_Plot_Temperature"] = (
                    predicted["_Actual_Temperature"].fillna(
                        fallback_temperature
                    )
                )

                predicted = predicted.dropna(
                    subset=["_Plot_Date", "_Plot_Temperature"]
                )

                if not predicted.empty:
                    predicted["_Temperature_Source"] = (
                        predicted["_Actual_Temperature"].apply(
                            lambda value: (
                                "Actual temperature used"
                                if pd.notna(value)
                                else "Actual temperature unavailable; marker uses fallback position"
                            )
                        )
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=predicted["_Plot_Date"],
                            y=predicted["_Plot_Temperature"],
                            mode="markers",
                            name="Predicted Heatwave",
                            marker=dict(
                                color="#54799F",
                                size=13,
                                symbol="circle-open",
                                line=dict(color="#54799F", width=2.5)
                            ),
                            customdata=predicted[
                                ["_Temperature_Source"]
                            ].to_numpy(),
                            hovertemplate=(
                                "<b>Predicted Heatwave</b><br>"
                                "Target date: %{x|%d %b %Y}<br>"
                                "Chart temperature: %{y:.1f} °C<br>"
                                "%{customdata[0]}"
                                "<extra></extra>"
                            )
                        )
                    )

    fig.update_layout(
        template="plotly_white",
        height=460,
        hovermode="closest",
        margin=dict(l=15, r=15, t=30, b=15),
        font=dict(
            family="Arial, sans-serif",
            color="#24364B",
            size=12
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(255,255,255,0)"
        ),
        xaxis_title="Date",
        yaxis_title="Maximum Temperature (°C)",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF"
    )

    fig.update_xaxes(
        range=[start_date, end_date],
        showgrid=True,
        gridcolor="#E8EDF3",
        linecolor="#DCE3EB",
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E8EDF3",
        linecolor="#DCE3EB",
        zeroline=False,
        autorange=True
    )

    if chart_actuals.empty:
        st.info(
            "No temperature observations are available in this period. "
            "Predicted heatwave markers can still appear if forecasts exist."
        )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 30-Day Observation Summary")

    temperatures = pd.to_numeric(
        chart_actuals["TMAX"], errors="coerce"
    ).dropna()

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Average Temperature",
            f"{temperatures.mean():.1f} °C"
            if not temperatures.empty else "N/A"
        )

    with metric2:
        st.metric(
            "Highest Temperature",
            f"{temperatures.max():.1f} °C"
            if not temperatures.empty else "N/A"
        )

    with metric3:
        st.metric("Days Recorded", str(len(temperatures)))

else:
    st.warning(
        "The historical dataset must contain LOCATION, DATE and TMAX columns. "
        "Check event_labeled_dataset.csv."
    )


# --------------------------------------------------
# MODEL PERFORMANCE COMPARISON
# --------------------------------------------------

st.markdown("---")
st.markdown("## Model Performance Comparison")

st.markdown(
    '<div class="subtitle">'
    'Compare Random Forest, Decision Tree and SVM across '
    'heatwave, drought and compound-event prediction.'
    '</div>',
    unsafe_allow_html=True
)

if comparison_df.empty:
    st.warning(
        "Model comparison file not found. "
        "Check results/model_comparison.csv."
    )

else:
    event_col = find_column(comparison_df, ["Event", "event"])
    model_col = find_column(comparison_df, ["Model", "model"])
    accuracy_col = find_column(comparison_df, ["Accuracy", "accuracy"])

    if not all([event_col, model_col, accuracy_col]):
        st.error(
            "The comparison file must include Event, Model and Accuracy columns."
        )
        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        comparison_df = comparison_df.rename(
            columns={
                event_col: "Event",
                model_col: "Model"
            }
        ).copy()

        comparison_df["Accuracy (%)"] = pd.to_numeric(
            comparison_df[accuracy_col], errors="coerce"
        )

        if (
            not comparison_df["Accuracy (%)"].dropna().empty
            and comparison_df["Accuracy (%)"].dropna().max() <= 1
        ):
            comparison_df["Accuracy (%)"] *= 100

        st.markdown("### Accuracy by Event and Model")

        model_colors = {
            "Random Forest": "#24364B",
            "Decision Tree": "#54799F",
            "SVM": "#9B493C"
        }

        fig_comparison = px.bar(
            comparison_df,
            x="Event",
            y="Accuracy (%)",
            color="Model",
            barmode="group",
            text="Accuracy (%)",
            color_discrete_map=model_colors,
            category_orders={
                "Model": ["Random Forest", "Decision Tree", "SVM"]
            }
        )

        fig_comparison.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
            cliponaxis=False
        )

        fig_comparison.update_layout(
            template="plotly_white",
            height=430,
            font=dict(
                family="Arial, sans-serif",
                color="#24364B",
                size=12
            ),
            yaxis_title="Accuracy (%)",
            xaxis_title="Event Type",
            yaxis_range=[0, 110],
            legend_title="Machine Learning Model",
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=15, r=15, t=30, b=15)
        )

        fig_comparison.update_xaxes(
            gridcolor="#E8EDF3",
            linecolor="#DCE3EB"
        )

        fig_comparison.update_yaxes(
            gridcolor="#E8EDF3",
            linecolor="#DCE3EB"
        )

        st.plotly_chart(
            fig_comparison,
            use_container_width=True
        )

        # ------------------------------------------
        # FILTERABLE DETAILED PERFORMANCE METRICS
        # ------------------------------------------

        st.markdown("### Detailed Performance Metrics")
        st.caption(
            "Choose the metrics you want to compare across events and models."
        )

        metric_names = {
            "Accuracy": ["Accuracy", "accuracy"],
            "Precision": ["Precision", "precision"],
            "Recall": ["Recall", "recall"],
            "F1-Score": ["F1-Score", "F1_Score", "F1", "f1-score"]
        }

        available_metric_columns = {}

        for display_name, possible_names in metric_names.items():
            source_col = find_column(comparison_df, possible_names)

            if source_col:
                available_metric_columns[display_name] = source_col

        if not available_metric_columns:
            st.warning(
                "No Accuracy, Precision, Recall or F1-Score columns "
                "were found in the comparison file."
            )
        else:
            selected_metrics = st.multiselect(
                "Select performance metrics",
                options=list(available_metric_columns.keys()),
                default=list(available_metric_columns.keys()),
                key="selected_performance_metrics",
                help="Select one or more metrics. Clear the selection to choose again."
            )

            if not selected_metrics:
                st.info("Select at least one metric to display the table.")
            else:
                display_df = comparison_df[["Event", "Model"]].copy()

                for display_name in selected_metrics:
                    source_col = available_metric_columns[display_name]

                    values = pd.to_numeric(
                        comparison_df[source_col], errors="coerce"
                    )

                    if (
                        not values.dropna().empty
                        and values.dropna().max() <= 1
                    ):
                        values = values * 100

                    display_df[display_name] = values.apply(
                        lambda value: (
                            f"{value:.2f}%"
                            if pd.notna(value) else "N/A"
                        )
                    )

                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )

        # ------------------------------------------
        # BEST MODEL PER EVENT
        # ------------------------------------------

        st.markdown("### Best Model for Each Event")

        valid_comparison = comparison_df.dropna(
            subset=["Accuracy (%)"]
        )

        if not valid_comparison.empty:
            best_models = valid_comparison.loc[
                valid_comparison.groupby("Event")["Accuracy (%)"].idxmax()
            ][["Event", "Model", "Accuracy (%)"]].copy()

            best_models = best_models.rename(
                columns={
                    "Model": "Best Performing Model",
                    "Accuracy (%)": "Accuracy"
                }
            )

            best_models["Accuracy"] = best_models["Accuracy"].apply(
                lambda value: f"{value:.2f}%"
            )

            st.dataframe(
                best_models,
                use_container_width=True,
                hide_index=True
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div class="dashboard-footer">
        <strong style="color:#344E70;">EXTREME EVENT WARNING SYSTEM</strong>
        <br>
        Climate Monitoring · Event Forecasting · Model Evaluation
    </div>
    """,
    unsafe_allow_html=True
)
