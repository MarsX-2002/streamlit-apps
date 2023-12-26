import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Simple Stock Price App

Shown are the stock **closing price** and **volume** of a chosen stock!
""")

# Add a link to your GitHub profile
st.markdown("Check out my [GitHub](https://github.com/MarsX-2002) profile! :joy:")

# Get user input for the ticker symbol
ticker_input = st.text_input("Enter the stock ticker symbol (e.g., AAPL):", "AAPL")

# get data on the chosen ticker
tickerData = yf.Ticker(ticker_input)
# get historical pricing for this ticker
tickerDf = tickerData.history(period='1d', start='2000-01-01', end='2024-01-01')

# Display the selected stock's closing price and volume
st.write(f"## {ticker_input} Closing Price")
st.line_chart(tickerDf.Close)

st.write(f"## {ticker_input} Volume")
st.line_chart(tickerDf.Volume)
