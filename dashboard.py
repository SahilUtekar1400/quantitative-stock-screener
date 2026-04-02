# 1. Importing all the required libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 3. Providing a frontend UI.
st.set_page_config(page_title="Financial Dashboard",layout="wide")
st.title("Ticker-Tracker for your financial tracking!")

# 2. Setting up the list for scalability
INDICIES = {
    "NSE (Nifty 50)" : ['ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 
           'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BEL.NS', 'BHARTIARTL.NS', 
           'CIPLA.NS', 'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ETERNAL.NS', 
           'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HINDALCO.NS', 
           'HINDUNILVR.NS', 'ICICIBANK.NS', 'ITC.NS', 'INFY.NS', 'INDIGO.NS', 
           'JSWSTEEL.NS', 'JIOFIN.NS', 'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 
           'MAXHEALTH.NS', 'NTPC.NS', 'NESTLEIND.NS', 'ONGC.NS', 'POWERGRID.NS', 
           'RELIANCE.NS', 'SBILIFE.NS', 'SHRIRAMFIN.NS', 'SBIN.NS', 'SUNPHARMA.NS', 
           'TCS.NS', 'TATACONSUM.NS', 'TMPV.NS', 'TATASTEEL.NS', 'TECHM.NS', 'TITAN.NS', 
           'TRENT.NS', 'ULTRACEMCO.NS', 'WIPRO.NS'],

    "BSE (Sensex 30)" : ['ADANIPORTS.BO', 'ASIANPAINT.BO', 'AXISBANK.BO', 'BAJFINANCE.BO', 
           'BAJAJFINSV.BO', 'BHARTIARTL.BO', 'HCLTECH.BO', 'HDFCBANK.BO', 'HINDUNILVR.BO', 
           'ICICIBANK.BO', 'INDUSINDBK.BO', 'INFY.BO', 'ITC.BO', 'KOTAKBANK.BO', 'LT.BO', 
           'M&M.BO', 'MARUTI.BO', 'NESTLEIND.BO', 'NTPC.BO', 'POWERGRID.BO', 'RELIANCE.BO', 
           'SBIN.BO', 'SUNPHARMA.BO', 'TCS.BO', 'TATAMOTORS.BO', 'TATASTEEL.BO', 'TECHM.BO', 
           'TITAN.BO', 'ULTRACEMCO.BO', 'WIPRO.BO'],
}

col1, col2 = st.columns(2)

with col1:
    selected_exchange = st.selectbox("Select Exchange",options=list(INDICIES.keys()))

with col2:
    # 4. Setting up a dropdown list for all symbols
    symbol = st.selectbox(label="Symbols",options=INDICIES[selected_exchange])

# 14. Senior Upgrade
@st.cache_data
def fetch_market_data(ticker):
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)

    query = f'SELECT * FROM "{ticker}"'
    df = pd.read_sql_query(query,engine,index_col='Date',parse_dates=['Date'])
    return df

# 8. Reading the data queried.
try:
    read_query = fetch_market_data(symbol)
except Exception as e:
    st.error(f"Data for {symbol} not found in the database. Kindly choose other option.")
# 10. Setting up the plot figure
fig = go.Figure()

# 11. Layering of candlestick with scatter plot for rolling average
fig.add_trace(go.Candlestick(x=read_query.index,
                            open= read_query['Open'],
                            high= read_query['High'],
                            low= read_query['Low'],
                            close= read_query['Close'],
                            name=f"{symbol} Historical Data"
                            ))

fig.add_trace(go.Scatter(
    x=read_query.index,
    y=read_query['SMA_50'],
    name='50 Rolling Avg',
    mode='lines',
    line=dict(
        color= 'blue',
        width= 2
    )
)) 

# 12. Providing title and other ui changes
fig.update_layout(
    title=f'Historical performance of {symbol} with 50 rolling avg',
    xaxis_title= 'Date',
    yaxis_title= 'Amount'
)

# 9. Checking the df loading properly or not
st.dataframe(read_query.tail(10))

# 13. Ploting the figure
st.plotly_chart(fig,use_container_width=True)