# 1. Importing all the required libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from plotly.subplots import make_subplots

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

    # 10. Visualization: Multi Panel Dashbaord
    # 3 row format
    # Row 1 is large (Price), Rows 2 & 3 are smaller (Indicators)
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6,0.2,0.2]
    )

    # Row 1: Candlestick & SMA
    # 11. Layering of candlestick with scatter plot for rolling average
    fig.add_trace(go.Candlestick(x=read_query.index,
                                open= read_query['Open'],
                                high= read_query['High'],
                                low= read_query['Low'],
                                close= read_query['Close'],
                                name=f"{symbol} Historical Data"
                                ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=read_query.index,
        y=read_query['SMA_50'],
        name='50 Rolling Avg',
        mode='lines',
        line=dict(
            color= 'blue',
            width= 2
        )
    ), row=1, col=1)

    # Row 2: RSI
    fig.add_trace(go.Scatter(
        x=read_query.index, y=read_query['RSI'],
        name=f'RSI for {symbol}', mode='lines', line=dict(color='purple',width=2)
    ), row=2, col=1)

    #Adding overbought/oversold refernce lines for RSI
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1) 

    # Row 3: MACD
    fig.add_trace(go.Scatter(
        x=read_query.index, y=read_query['MACD'],
        name=f'MACD for {symbol}', mode='lines', line=dict(color='orange',width=2)
    ),row=3, col=1)

    fig.add_trace(go.Scatter(
        x=read_query.index, y=read_query['Signal_Line'],
        name=f'Signal Line for {symbol}', mode='lines', line=dict(color='cyan',width=2)
    ), row=3, col=1)

    # MACD Histogram
    fig.add_trace(go.Bar(
        x=read_query.index, y=read_query['MACD_Histogram'],
        name=f'Histogram for {symbol}', marker_color='gray'
    ), row=3, col=1)

    # 12. Providing title and other ui changes
    fig.update_layout(
        title=f'Quantitative Analysis: {symbol}',
        height=800,
        template='plotly_dark',
        showlegend=True,
        xaxis_rangeslider_visible=False
    )

    # 9. Checking the df loading properly or not
    st.dataframe(read_query.tail(10))

    # 13. Ploting the figure
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Data for {symbol} not found in the database. Kindly choose other Symbol.")

