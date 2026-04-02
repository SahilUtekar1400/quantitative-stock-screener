import os
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Loading the security perimeter (reads the .env file)
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

#Check if the URL loaded correctly to prevent silent failure
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found. Check your .env file.")

# Build the SQLAlchemy Engine (The Cloud Pipeline)
# replacing sqlite3.connect()
engine = create_engine(DATABASE_URL)

symbols = ["RELIANCE.NS","HDFCBANK.NS"]


for symbol in symbols:
    stock = yf.Ticker(symbol)
    data = stock.history(period="2y")

    data['SMA_50'] = data['Close'].rolling(window=50).mean()

    data.to_sql(symbol,engine,if_exists='replace')
    print(f"Successfully pushed {symbol} to Supbase PostgreSQL.")
