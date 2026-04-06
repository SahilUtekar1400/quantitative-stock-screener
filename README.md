# Quantitative Screener, Automated ETL & Predictive ML Pipeline

## Overview
This project is an end-to-end quantitative financial pipeline. It features a fully automated ETL architecture extracting daily data for the NIFTY 50 and SENSEX 30 indices, advanced feature engineering for technical indicators, a cloud-hosted relational database, and a multi-panel reactive dashboard. Currently, it includes an active Machine Learning sandbox for predictive price modeling.

## The Architecture
The system is decoupled into discrete, scalable micro-layers:

### 1. Extraction & Automation (Fault-Tolerant ETL)
* **Scale:** Bulk downloads historical daily market data for 80 Indian equities (NSE & BSE).
* **Automation:** GitHub Actions CI/CD executes a serverless cron job daily at market close.
* **Fault Tolerance:** Built-in `try/except` quarantine protocols ensure the pipeline survives API rate limits, missing tickers, or network drops without fatal crashes.

### 2. Quantitative Transformation (Feature Engineering)
Translates raw price action into multi-dimensional algorithmic signals using Pandas.
* **Trend & Lag Management:** Utilizes Exponential Weighted Moving Averages (EMA) via `ewm()` rather than standard Simple Moving Averages (SMA) to eliminate lag on reversal signals.
* **Momentum:** Relative Strength Index (RSI - 14 Day).
* **Trend Reversal:** Moving Average Convergence Divergence (MACD & Signal Line).
* **Risk:** 20-Day Standard Deviation (Volatility).

### 3. Storage (Cloud PostgreSQL)
* Replaces ephemeral local storage with a persistent **Supabase PostgreSQL** cloud vault.
* Utilizes `SQLAlchemy` and `psycopg2` with connection pooling to manage network routing and secure environment variable integration.

### 4. Client Interface (Streamlit & Plotly Subplots)
* **Cascading UI:** Dynamic exchange-to-ticker dropdown logic.
* **Scale-Collapse Prevention:** Utilizes Plotly's `make_subplots` to render a synchronized, 3-panel visual hierarchy. This prevents massive price scales from crushing smaller momentum oscillators (RSI/MACD) by assigning independent Y-axes while locking a shared chronological X-axis.

### 5. Predictive Analytics (Machine Learning Sandbox)
* **Algorithm:** Random Forest Regressor (`scikit-learn`).
* **Objective:** Predicting $T+1$ (Tomorrow's) closing price based on today's multidimensional signals (Price, RSI, MACD, Volatility).
* **Time-Series Integrity:** Strict `shuffle=False` train-test splitting to prevent future data leakage during model training.

## Tech Stack
* **Language:** Python 3.10+
* **Data & Math:** Pandas, Scikit-Learn
* **Database:** PostgreSQL (Supabase Cloud), SQLAlchemy
* **Visualization:** Plotly Graph Objects, Matplotlib
* **Deployment:** Streamlit Community / Render, GitHub Actions (YAML CI/CD)

## How to Run Locally

**1. Clone the repository:**
```bash
git clone [https://github.com/YOUR-USERNAME/quantitative-stock-screener.git](https://github.com/YOUR-USERNAME/quantitative-stock-screener.git)
cd quantitative-stock-screener
```

**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables:**
* Create a file named exactly (`.env`) in the root directory.
* Add your PostgreSQL connection string:
```bash
DATABASE_URL="postgresql://username:password@your-database-host:6543/postgres"
```

**4. Populate the Database (First Run):**
```bash
Populate the Database (First Run):
```

**5. Execute the ML Sandbox (Local Prediction):**
```bash
python ml_sandbox.py
```

**6. Launch the Dashboard:**
```bash
Launch the Dashboard:
```

**Author**
-Sahil Utekar Building Quantitative Data Engineering & Machine Learning.