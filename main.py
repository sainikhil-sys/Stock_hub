import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import requests
from dotenv import load_dotenv
import os
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

st.set_page_config(page_title="📊 Stock Market Live Dashboard", layout="wide")
st.title("📈 Stock Market Live Dashboard")

# Select stocks
stock_options = {
    "Sensex (BSE)": "^BSESN",
    "Nifty 50 (NSE)": "^NSEI",
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "Wipro": "WIPRO.NS",
    "HDFC Bank": "HDFCBANK.NS"
}

selected_stocks = st.multiselect("Select stocks/indexes to compare:", list(stock_options.keys()), default=["Sensex (BSE)"])
interval = st.selectbox("Time Interval", ["1m", "5m", "15m", "1h"], index=0)

# Fetch and plot data
for stock in selected_stocks:
    symbol = stock_options[stock]
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval=interval)

    if not data.empty:
        # Calculate moving averages
        data["MA20"] = data["Close"].rolling(window=20).mean()
        data["MA50"] = data["Close"].rolling(window=50).mean()

        st.subheader(f"{stock} - Live Chart")

        # Price chart with moving averages
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Price', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='MA 20', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name='MA 50', line=dict(color='green')))
        fig.update_layout(title=f"{stock} Price Chart", xaxis_title='Time', yaxis_title='INR', height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Volume chart
        st.subheader(f"{stock} - Volume")
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color='purple'))
        fig_vol.update_layout(height=250, xaxis_title='Time', yaxis_title='Volume')
        st.plotly_chart(fig_vol, use_container_width=True)
    else:
        st.warning(f"No data found for {stock}.")

# News Section
st.header("🗞️ Latest Financial News")
if NEWS_API_KEY:
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        articles = response.json().get("articles", [])

        for article in articles[:5]:
            st.markdown(f"### [{article['title']}]({article['url']})")
            st.write(article['description'])
            st.write("---")
    except Exception as e:
        st.error("Error fetching news.")
else:
    st.warning("News API key missing. Please set `NEWS_API_KEY` in your .env file.")
