import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the model
model = joblib.load("models/xgb_demand_model.joblib")

# Load Hourly threshold values for demand buckets
thresholds = pd.read_csv("reports/hourly_demand_thresholds.csv")

st.title("Electricity Demand Forecasting")
st.markdown("Enter the details to forecast electricity demand for the next hour")

# Input Form
col1, col2 = st.columns(2)
with col1:
    hour = st.number_input("Hour of Day (0-23)", 0, 23, 12)
    temperature = st.number_input("Temperature (°C)", -30, 50, 20)
with col2:
    day_of_week = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    month = st.selectbox("Month", list(range(1, 13)))

# Default values for input fields
default_values = pd.read_csv("reports/app_demand_defaults.csv")
input_row = default_values.copy()

# Mapping
day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
day_num = day_map[day_of_week]

# Update with user inputs
input_row['temperature'] = temperature
input_row['hour'] = hour
input_row['month'] = month
input_row['day_of_week'] = day_num
input_row['is_weekend'] = 1 if day_num >= 5 else 0

# Cyclical features
input_row['hour_sin'] = np.sin(2 * np.pi * hour / 24)
input_row['hour_cos'] = np.cos(2 * np.pi * hour / 24)
input_row['dow_sin'] = np.sin(2 * np.pi * day_num / 7)
input_row['dow_cos'] = np.cos(2 * np.pi * day_num / 7)
input_row['month_sin'] = np.sin(2 * np.pi * month / 12)
input_row['month_cos'] = np.cos(2 * np.pi * month / 12)

if st.button("Predict Demand"):
    feature_cols = feature_cols = [
    'temperature', 'is_weekend', 'lag_24', 'lag_48', 'lag_168',
    'rolling_mean_3', 'rolling_mean_24', 'rolling_std_24', 'rolling_mean_168',
    'temp_lag_1', 'temp_lag_3', 'temp_lag_24',
    'hour_sin', 'hour_cos', 'dow_sin', 'dow_cos', 'month_sin', 'month_cos'
    ]
    X_input = input_row[feature_cols]

    # Predict
    predicted_demand = model.predict(X_input)[0]

    # Get hourly thresholds
    hour_thresh = thresholds[thresholds['hour'] == hour].iloc[0]

    # Determine Alert Level
    if predicted_demand >= hour_thresh['p99']:
        alert = "🚨 Critical"
        action = "Emergency load shedding required"
        color = "error"
    elif predicted_demand >= hour_thresh['p90']:
        alert = "🔴 High Alert"
        action = "Activate reserve capacity immediately"
        color = "error"
    elif predicted_demand >= hour_thresh['p75']:
        alert = "🟡 Elevated"
        action = "Monitor closely, prepare reserves"
        color = "warning"
    elif predicted_demand >= hour_thresh['p25']:
        alert = "🟢 Normal"
        action = "Standard operations"
        color = "success"
    else:
        alert = "🔵 Low Demand"
        action = "Good window for maintenance"
        color = "info"

    # Display results
    st.markdown("---")
    st.subheader("Forecast Result")
    st.metric("Predicted Demand", f"{predicted_demand:,.0f} MW")
    
    getattr(st, color)(f"**{alert}** — {action}")

    # Compare to hourly average
    diff = predicted_demand - hour_thresh['mean']
    direction = "above" if diff > 0 else "below"
    st.caption(f"Predicted demand is {abs(diff):,.0f} MW {direction} the historical average for hour {hour}")
    st.markdown("---")
    st.caption(f"Hour {hour} thresholds — Normal range: {hour_thresh['p25']:,.0f} - {hour_thresh['p75']:,.0f} MW | High Alert above: {hour_thresh['p90']:,.0f} MW | Critical above: {hour_thresh['p99']:,.0f} MW")
    



