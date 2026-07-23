# Weather Trend Forecasting

**PM Accelerator Technical Assessment — Data Science / Analyst Track**

## PM Accelerator Mission

> PM Accelerator supports aspiring and current product professionals — including AI/data practitioners — in building real, hands-on portfolio projects and developing the skills needed to break into and grow in tech careers, backed by mentorship and an active community.

---

## 1. Project Overview

This project analyzes the **Global Weather Repository** dataset (Kaggle) to identify weather and climate trends, understand relationships between weather variables, and build models that forecast future temperature. The work covers both the basic and advanced tracks of the assessment:

- Data cleaning & preprocessing
- Exploratory data analysis (EDA)
- Anomaly detection
- Multi-model forecasting with an ensemble
- Climate, spatial, and geographic analysis
- Feature importance analysis

**Dataset:** [World Weather Repository](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository/code) — 154,751 rows, 41 features, hourly-updated readings for 211 countries, spanning ~2 years (May 2024 – July 2026).

## 2. Objectives

- Clean and prepare the data for analysis.
- Perform EDA to identify trends and relationships between variables (temperature, precipitation, air quality, etc.).
- Build and evaluate multiple forecasting models for daily average temperature, using `last_updated` as the time axis.
- Compare model performance with proper time-series validation (no data leakage from shuffling).
- Run additional advanced analyses: anomaly detection, feature importance, and spatial/geographic patterns.

## 3. Repository Structure

```
.
├── Weather_6_corrected.ipynb   # Main analysis notebook (cleaning → EDA → forecasting → feature importance)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 4. Methodology

### 4.1 Data Cleaning & Preprocessing
- **Duplicates:** checked both on full-row duplication and on a semantic key (latitude, longitude, `last_updated`); one hidden duplicate was found and removed.
- **Mixed-language labels:** country names were standardized across English, Russian, Chinese, Portuguese, German, and Arabic variants (4,318 rows fixed; 211 → 192 unique countries).
- **Redundant features:** a correlation matrix identified 7 columns with near-perfect (≥0.99) correlation to another column (e.g., °F duplicating °C, kph duplicating mph) — these were dropped, reducing the feature set from 41 to 34 columns.
- **Outliers & missing values:** a single reusable function, `cap_and_impute()`, caps out-of-range values to `NaN` and then either drops the affected rows (if under 5% of the data) or fills them with the country-level median (if 5% or more). It was applied to:
  - Air quality readings (physically impossible negative values)
  - Wind speed and pressure (capped at real-world record extremes)
  - Air quality readings again, using a 3×IQR upper bound (wider than the standard 1.5× to avoid discarding genuine pollution spikes, since there's no official sensor ceiling)

### 4.2 Exploratory Data Analysis
- Global daily average temperature and daily total precipitation, visualized as time series (plus a histogram for precipitation, since it is highly skewed).
- Correlation heatmap (filtered at |corr| ≥ 0.4) to surface meaningful relationships.

### 4.3 Advanced EDA — Climate & Geography
- Countries mapped to continents (via `pycountry_convert`, with a small manual patch for territories it doesn't recognize).
- Average temperature and PM2.5 by continent.
- Northern vs. Southern hemisphere monthly temperature, tracked separately (averaging globally would hide that seasons run opposite between hemispheres).
- Spatial scatter plots (latitude/longitude, colored by temperature and PM2.5) as a lightweight substitute for a full GIS map.
- Monthly global temperature trend over the full period, to see the seasonal cycle independent of daily noise.

### 4.4 Anomaly Detection
Three unsupervised methods were applied to the daily global average temperature series and compared for agreement (there is no labeled ground truth for global weather anomalies):
1. **Robust z-score (MAD)** — flagged 1 anomalous day.
2. **Isolation Forest** — flagged 16 anomalous days.
3. **Local Outlier Factor** — flagged 13 anomalous days.

Days flagged by both Isolation Forest and LOF (7 days) are treated as the strongest anomaly candidates.

### 4.5 Feature Engineering & Selection
Forecasting features: `lag_1`, `lag_2`, `lag_3`, `lag_7` (previous 1/2/3/7 days), `rolling_mean_7` (trailing 7-day average), `day_of_year`, and `month`.

Three feature-selection methods (variance threshold, `SelectKBest` with mutual information, and RFE) were compared against using all 6 features. None reduced RMSE by a meaningful margin — `lag_1` and `rolling_mean_7` were consistently ranked most important by every method — so the full feature set was kept.

### 4.6 Forecasting Models
Global daily average temperature was forecast using a chronological 80/20 train/test split (no shuffling, to avoid leaking future information). Seven approaches were compared, including two naive baselines:

| Model | MAE | RMSE | R² |
|---|---|---|---|
| **Linear Regression** | 0.313 | 0.384 | 0.977 |
| Ensemble (average of LR/RF/GB) | 0.319 | 0.388 | 0.977 |
| Naive (persistence: "tomorrow = today") | 0.315 | 0.398 | 0.976 |
| Gradient Boosting | 0.340 | 0.411 | 0.974 |
| Random Forest | 0.358 | 0.445 | 0.970 |
| Seasonal Naive (last week) | 0.580 | 0.738 | 0.916 |
| Prophet | 1.321 | 1.529 | 0.641 |
| ARIMA | 3.816 | 4.527 | -2.146 |

Random Forest and Gradient Boosting were tuned with `GridSearchCV` using `TimeSeriesSplit` (not a random k-fold) to keep the cross-validation chronological. ARIMA order was selected by AIC grid search; Prophet used default yearly/weekly seasonality.

**Robustness check:** because a single 80/20 split is only one snapshot of "the future," a 5-fold rolling-window time-series cross-validation was also run. Under that check, **Naive (persistence)** — not Linear Regression — comes out on top, showing that the single-split "winner" doesn't fully hold up. This discrepancy is reported directly rather than hidden.

### 4.7 Feature Importance
Two complementary techniques were applied to the Random Forest / Gradient Boosting models:
1. **Built-in (impurity-based) importance** — fast, but biased toward high-cardinality continuous features like the lags.
2. **Permutation importance** — model-agnostic, measures the actual increase in error when a feature is shuffled.

Both methods agree: `lag_1` (yesterday's temperature) dominates, with `rolling_mean_7` a distant second.

## 5. Key Insights

- **Yesterday's temperature is the single strongest predictor** of tomorrow's — confirmed independently by feature selection, impurity-based importance, and permutation importance.
- **A naive "tomorrow = today" baseline is very hard to beat** on this series; the more sophisticated models only match it, and cross-validation shows it may actually be the safer choice over the single-split "winner."
- **Seasonality is real but hemisphere-dependent** — averaging temperature globally hides the fact that seasons run in opposite directions north vs. south of the equator.
- **Anomaly detection benefits from agreement across methods** rather than trusting any single method, since there is no ground truth to validate against.

## 6. Known Limitations

- Forecasting targets a single aggregated global daily-average series rather than per-location series; per-city forecasting was out of scope here but is the natural next step.
- ARIMA and Prophet are univariate and ignore humidity, wind, and air quality entirely, unlike the regression-based models.
- The model persisted to disk is chosen by the single 80/20 split, even though the cross-validation robustness check suggests the naive baseline generalizes better — this trade-off is noted in the notebook for transparency.
- Group-median imputation for outlier treatment is computed over the full dataset rather than the training split only, which is a mild source of information leakage for the time-series forecasting task (though it affects a very small fraction of rows).

## 7. How to Run

### Requirements
See `requirements.txt`. Core libraries: `pandas`, `numpy`, `scikit-learn`, `xgboost`, `statsmodels`, `prophet`, `pycountry-convert`, `kagglehub`, `matplotlib`, `seaborn`, `scipy`, `joblib`.

### Setup
```bash
# Clone the repository
git clone https://github.com/tank550/Weather-Trend-Forecasting
cd Weather-Trend-Forecasting/datascience

# (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the notebook
```bash
jupyter notebook weather.ipynb
```
Run all cells top to bottom. The notebook downloads the dataset automatically via `kagglehub` on first run (a Kaggle account / API token may be required — see [kagglehub docs](https://github.com/Kaggle/kagglehub) if the download step prompts for authentication). The best-performing model is saved to `best_weather_model.joblib` at the end of the forecasting section.

## 8. Author's Note

This notebook was built iteratively: several sections (e.g., outlier handling, scaling) were refactored from an earlier draft into single reusable functions once repeated patterns were noticed, and the cross-validation section was added specifically to stress-test the single-split model comparison rather than take it at face value. Both the strengths and the limitations above are reported as found, without smoothing over the parts that didn't resolve cleanly.
