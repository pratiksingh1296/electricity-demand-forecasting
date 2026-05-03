# Electricity Demand Forecasting

Predicting hourly electricity demand using time-series feature engineering and machine learning models.

---

## Overview

Electricity demand exhibits strong temporal patterns driven by daily cycles, weekly behavior, and weather conditions.
This project builds an end-to-end forecasting pipeline to predict hourly electricity demand using historical load and temperature data.

The objective is to develop models that improve upon a seasonal baseline and capture nonlinear relationships in demand patterns.

---

## Problem Statement

* **Target:** Hourly electricity demand (MW)
* **Horizon:** Short-term forecasting
* **Use case:** Grid operators for demand planning and resource allocation

---

## Dataset

* **Source:** EIA Grid Monitor (Texas region) + Open-Meteo weather data
* **Granularity:** Hourly
* **Time Range:** 2018 – 2023

### Features

* Historical demand (lag features)
* Rolling statistics (short & long-term trends)
* Weather (temperature + lagged temperature)
* Calendar features (hour, day, month)
* Cyclical encoding of time features

---

## Feature Engineering

Key transformations:

* **Lag Features:** `lag_24`, `lag_48`, `lag_168`
* **Rolling Features:** moving averages and standard deviation
* **Cyclical Encoding:**

  * hour → sin/cos
  * day_of_week → sin/cos
  * month → sin/cos
* **Weather Features:** temperature + lagged temperature

These features capture seasonality, trends, and external drivers of demand.

---

## Models

The following models were evaluated:

1. **Seasonal Naive (Baseline)** – previous day demand
2. **Linear Regression** – strong baseline with engineered features
3. **Decision Tree** – captures nonlinear splits (overfitting observed)
4. **Random Forest** – reduces variance via ensemble averaging
5. **XGBoost** – gradient boosting for improved accuracy

---

## Results

| Model             | MAE (MW)  | MAPE (%)  |
| ----------------- | --------- | --------- |
| Baseline (Lag-24) | ~2299     | ~4.65     |
| Linear Regression | ~1673     | ~3.28     |
| Decision Tree     | ~1929     | ~3.57     |
| Random Forest     | ~1426     | ~2.53     |
| **XGBoost**       | **~1360** | **~2.40** |

---

## Key Visualizations

### Model Comparison
![Model Comparison](reports/figures/model_comparison_mae.png)

### Final Predictions (Actual vs Models)
![Predictions](reports/figures/final_predictions_comparison.png)

### Feature Importance (XGBoost)
![Feature Importance](reports/figures/feature_importance_xgb.png)

---

## Key Insights

* Electricity demand shows strong **daily and weekly seasonality**
* Lag features (especially **lag_24**) are highly predictive
* Temperature significantly impacts demand (nonlinear effect)
* **Feature engineering is critical** — even linear models perform well
* Ensemble methods outperform individual models:

  * Random Forest reduces overfitting
  * XGBoost captures complex interactions and performs best

---

## Conclusion

The XGBoost model achieves the best performance, significantly improving over the seasonal baseline.

This project demonstrates that combining **domain-aware feature engineering with ensemble models** leads to accurate and robust electricity demand forecasts.

---

## Future Improvements

* Use **weather forecasts** instead of historical temperature
* Implement **rolling cross-validation**
* Extend to **multi-step forecasting**
* Add **uncertainty estimation (prediction intervals)**

---

## Project Structure

```
electricity-demand-forecasting/
│
├── notebooks/
│   ├── 01_datasanity.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_baseline.ipynb
│   └── 04_ml_models.ipynb
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   ├── figures/
│   └── summary_tables/
│
├── src/
├── README.md
└── requirements.txt
```

---

## How to Run

1. Clone the repository
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run notebooks in order:

```
01 → 02 → 03 → 04
```

---

## Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* XGBoost
* Matplotlib

---

## 📌 Author

Pratik Singh

Aspiring Data Scientist with a focus on machine learning, time-series forecasting, and building end-to-end data projects.


## 📊 Dataset

* **Source:**

  * Electricity Demand: EIA Grid Monitor (Texas region)
  * Weather Data: Open-Meteo API

* **Granularity:** Hourly

* **Time Range:** 2018 – 2023

---

### Electricity Demand Data

The electricity demand data is sourced from the EIA Grid Monitor for the Texas region and contains:

* Actual hourly demand (MW)
* Forecasted demand (MW)
* Timestamp (local time)

Due to file size constraints, the raw demand dataset is **not included** in this repository.

To reproduce the project:

1. Download the data from: https://www.eia.gov/electricity/gridmonitor/
2. Select the Texas region and export hourly data
3. Place the file in: `data/raw/`

---

### Weather Data

Weather data is obtained using the Open-Meteo API and is included in this repository.

It contains:

* Hourly temperature (`temperature_2m`)
* Timestamp aligned with demand data

This data is used to capture the impact of weather on electricity demand.

---

### Data Processing

* Timestamps are aligned and merged between demand and weather datasets
* Missing values are handled via interpolation
* Duplicate timestamps (e.g., due to DST) are resolved
* Final dataset is stored in `data/processed/`

---

### Target Variable

* **`demand_MW`** → Hourly electricity demand in megawatts

---

### Key Challenges

* Strong daily and weekly seasonality
* Weather-driven variability
* Time alignment across multiple data sources
* Handling missing and duplicate timestamps
