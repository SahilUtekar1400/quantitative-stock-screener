import os
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import time

# Loading the security perimeter (reads the .env file)
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

#Check if the URL loaded correctly to prevent silent failure
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found. Check your .env file.")

# Build the SQLAlchemy Engine (The Cloud Pipeline)
# replacing sqlite3.connect()
engine = create_engine(DATABASE_URL)

sensex_30=['ADANIPORTS.BO', 'ASIANPAINT.BO', 'AXISBANK.BO', 'BAJFINANCE.BO', 
           'BAJAJFINSV.BO', 'BHARTIARTL.BO', 'HCLTECH.BO', 'HDFCBANK.BO', 'HINDUNILVR.BO', 
           'ICICIBANK.BO', 'INDUSINDBK.BO', 'INFY.BO', 'ITC.BO', 'KOTAKBANK.BO', 'LT.BO', 
           'M&M.BO', 'MARUTI.BO', 'NESTLEIND.BO', 'NTPC.BO', 'POWERGRID.BO', 'RELIANCE.BO', 
           'SBIN.BO', 'SUNPHARMA.BO', 'TCS.BO', 'TATAMOTORS.BO', 'TATASTEEL.BO', 'TECHM.BO', 
           'TITAN.BO', 'ULTRACEMCO.BO', 'WIPRO.BO']

nifty_50= ['ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 
           'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BEL.NS', 'BHARTIARTL.NS', 
           'CIPLA.NS', 'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ETERNAL.NS', 
           'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HINDALCO.NS', 
           'HINDUNILVR.NS', 'ICICIBANK.NS', 'ITC.NS', 'INFY.NS', 'INDIGO.NS', 
           'JSWSTEEL.NS', 'JIOFIN.NS', 'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 
           'MAXHEALTH.NS', 'NTPC.NS', 'NESTLEIND.NS', 'ONGC.NS', 'POWERGRID.NS', 
           'RELIANCE.NS', 'SBILIFE.NS', 'SHRIRAMFIN.NS', 'SBIN.NS', 'SUNPHARMA.NS', 
           'TCS.NS', 'TATACONSUM.NS', 'TMPV.NS', 'TATASTEEL.NS', 'TECHM.NS', 'TITAN.NS', 
           'TRENT.NS', 'ULTRACEMCO.NS', 'WIPRO.NS']

all_symbols = nifty_50 + sensex_30


for symbol in all_symbols:
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="2y")

        if data.empty:
            print(f"Warning: No data found for {symbol}. Skipping.")
            continue

        # Feature Engineering
        # 1. Trend analysis: 50 day moving avg.
        data['SMA_50'] = data['Close'].rolling(window=50).mean()

        # 2. Risk analysis: 20 day volatility (Standard Deviation)
        data['Volatility'] = data['Close'].rolling(window=20).std()

        # 3. Momentum analysis: Relative Strength Index (RSI - 14 days)
        delta = data['Close'].diff()
        avg_gain = delta.where(delta>0,0).ewm(alpha=1/14, adjust=False).mean()
        avg_loss = (-delta.where(delta<0,0)).ewm(alpha=1/14, adjust=False).mean()
        rs = avg_gain/avg_loss
        data['RSI'] = 100 - (100 / (1 + rs))

        # 4. Trend Reversal: MACD (12 day EMA, 26 day EMA, 9 day signal)
        ema_12d = data['Close'].ewm(span=12, adjust=False).mean()
        ema_26d = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = ema_12d - ema_26d
        data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
        data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']

        # Droping NaN values created using rolling window
        data.dropna()

        data.to_sql(symbol,engine,if_exists='replace')
        print(f"Successfully pushed {symbol} to Supbase PostgreSQL.")

        time.sleep(2)
    
    except Exception as e:
        print(f"Failed to process {symbol}: {e}")

print("Daily extraction complete.")
