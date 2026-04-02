import sqlite3
import pandas as pd

conn = sqlite3.connect("market_data.db")

query = 'SELECT * FROM "RELIANCE.NS"'

reliance_data = pd.read_sql_query(query,conn,index_col='Date',parse_dates=['Date'])

conn.close()

print(reliance_data.tail())