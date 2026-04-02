# Quantitative Stock Screener & Financial Dashboard

## Overview
This project is an automated end-to-end data pipeline and interactive web dashboard. It replaces manual spreadsheet data entry with a robust ETL (Extract, Transform, Load) architecture designed to capture historical market data, engineer technical indicators, and serve them via a reactive UI.

## The Architecture
Unlike static data visualization scripts, this application separates the data extraction, database storage, and front-end rendering into discrete, scalable layers.

1. **Extraction (API):** Connects to the `yfinance` API to bulk-download historical daily market data for a portfolio of equities.
2. **Transformation (Pandas):** Flattens multi-index API responses into relational data structures and calculates rolling statistical features (e.g., 50-Day Moving Average).
3. **Storage (SQLite):** Writes the cleaned, time-series data into a local relational database (`market_data.db`), ensuring data persistence and eliminating redundant API calls.
4. **Visualization (Streamlit & Plotly):** A reactive web UI that queries the SQLite database directly. It utilizes `@st.cache_data` to store query results in RAM for instant rendering, and deploys fluid, responsive candlestick charts.

## Tech Stack
* **Language:** Python
* **Data Manipulation:** Pandas
* **Database:** SQLite3
* **Visualization:** Plotly Graph Objects
* **Web Framework:** Streamlit
* **Market Data Provider:** Yahoo Finance API (`yfinance`)

## Key Features
* **Automated Data Capture:** Dynamic time-window extraction (rolling 2-year history) avoiding hardcoded calendar constraints.
* **Database Caching:** Secure read/write SQL operations with Streamlit memory caching to prevent I/O bottlenecks and API rate-limiting.
* **Interactive Candlestick Charting:** Professional-grade visual layout featuring zoom, pan, and hover-state metrics, overlaid with engineered technical signals.
* **Responsive UI:** Dynamic container sizing ensures the dashboard scales cleanly across desktop and mobile environments.

## How to Run Locally

**1. Clone the repository:**
```bash
git clone [https://github.com/SahilUtekar1400/quantitative-stock-screener.git](https://github.com/SahilUtekar1400/quantitative-stock-screener.git)
cd quantitative-stock-screener
```
**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```
**3. Launch the Dashboard:**
```bash
streamlit run dashboard.py
```
