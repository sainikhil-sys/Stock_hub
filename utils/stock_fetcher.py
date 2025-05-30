import streamlit as st
import plotly.graph_objs as go
import yfinance as yf
from datetime import datetime, timedelta

def display_live_stock_graphs():
    st.subheader("📈 Real-time NSE Stocks / Indices")

    stock = st.selectbox("Select NSE Symbol (e.g., RELIANCE.NS, INFY.NS)", ['RELIANCE.NS', 'INFY.NS', 'HDFCBANK.NS', '^NSEI', '^BSESN'])

    data = yf.download(stock, period='1d', interval='5m', progress=False)
    if data.empty:
        st.error("No data available. Try another stock.")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price', line=dict(color='royalblue')))
    fig.update_layout(title=f"Live Chart: {stock}", xaxis_title='Time', yaxis_title='Price (INR)', height=500)

    st.plotly_chart(fig, use_container_width=True)

    # Auto-refresh every 60 seconds
    st.experimental_rerun() if st.button("🔁 Refresh Chart") else None
