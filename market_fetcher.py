import yfinance as yf
import pandas as pd
import sqlite3

symbols = ["RELIANCE.NS","HDFCBANK.NS"]

conn = sqlite3.connect('market_data.db')

for symbol in symbols:
    stock = yf.Ticker(symbol)

    data = stock.history(period="2y")

    data['SMA_50'] = data['Close'].rolling(window=50).mean()

    data.to_sql(symbol,conn,if_exists='replace')


conn.close()