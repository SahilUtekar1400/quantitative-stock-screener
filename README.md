# Quantitative Stock Screener & Automated ETL Pipeline

## Overview
This project is a fully automated, cloud-hosted ETL (Extract, Transform, Load) data pipeline and interactive financial dashboard. It is designed to capture market data, engineer technical indicators, and serve them via a reactive web interface with zero manual intervention.

## The Architecture
This application utilizes a decoupled, enterprise-grade architecture, separating the backend automation from the frontend client.

1. **Extraction (GitHub Actions & yfinance):** A CI/CD cron job wakes up an Ubuntu server daily at market close (12:00 PM UTC / 5:30 PM IST). It queries the Yahoo Finance API to extract the latest daily market data for a target portfolio.
2. **Transformation (Pandas):** The data is processed in-memory to standardize time-series indices and engineer rolling statistical features (e.g., 50-Day Moving Average).
3. **Storage (Supabase PostgreSQL):** Using `SQLAlchemy` and `psycopg2`, the script securely connects to a Supabase connection pooler and pushes the transformed data into a persistent cloud PostgreSQL database.
4. **Visualization (Streamlit & Plotly):** A reactive web UI hosted on Render directly queries the Supabase vault. It utilizes in-memory caching to prevent database bottlenecking and deploys fluid, responsive candlestick charts for technical analysis.

## Tech Stack
* **Language:** Python 3.10+
* **Data Manipulation:** Pandas
* **Database:** PostgreSQL (Supabase Cloud)
* **ORM / Database Adapters:** SQLAlchemy, psycopg2-binary
* **Visualization:** Plotly Graph Objects
* **Web Framework:** Streamlit (Deployed on Render)
* **Automation:** GitHub Actions (YAML CI/CD)

## Key Features
* **Zero-Touch Automation:** Daily data extraction and database updates run entirely in the background via GitHub Actions.
* **Cloud Database Engineering:** Transitioned from ephemeral local SQLite storage to persistent PostgreSQL utilizing connection pooling for optimized network routing.
* **Secure Credential Management:** Database URIs and passwords are strictly managed via environment variables (`.env`) and GitHub Secrets, ensuring zero credential leakage in the source code.
* **Interactive Candlestick Charting:** Professional-grade visual layout featuring zoom, pan, and hover-state metrics, overlaid with algorithmic trendlines.

## How to Run Locally

If you wish to clone and run this architecture on your local machine, follow these steps strictly to ensure database security.

**1. Clone the repository:**
```bash
git clone [https://github.com/SahilUtekar1400/quantitative-stock-screener.git](https://github.com/SahilUtekar1400/quantitative-stock-screener.git)
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

**5. Launch the Dashboard:**
```bash
Launch the Dashboard:
```

**Author**
-Sahil Utekar Building quantitative data pipelines and automated analytical tools.