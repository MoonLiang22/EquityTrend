#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 00:14:31 2024

@author: moonliang
"""
import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

#Stocks
stocks = ["AAPL", "MSFT", "AMZN", "GOOGL", "JNJ", "JPM", "XOM", "NVDA", "WMT","CHWY"]

#Streamlit dashboard
st.title("Stock Data Analysis Dashboard")

selected_stock = st.selectbox('Select stock', stocks)
start_date = st.date_input('Start date', pd.to_datetime('2019-06-23'))
end_date = st.date_input('End date', pd.to_datetime('2024-06-23'))

if st.button('Fetch Data'):
    #Stock prices and trading volumes
    data = yf.download(selected_stock, start=start_date, end=end_date)

    #Moving averages
    data['50-day MA'] = data['Close'].rolling(window=50).mean()
    data['200-day MA'] = data['Close'].rolling(window=200).mean()

    # Calculate RSI and MACD
    data['RSI'] = ta.momentum.RSIIndicator(close=data['Close'], window=14).rsi()
    macd = ta.trend.MACD(close=data['Close'], window_slow=26, window_fast=12, window_sign=9)
    data['MACD'] = macd.macd()
    data['MACD Signal'] = macd.macd_signal()
    data['MACD Diff'] = macd.macd_diff()

    #Volatility
    std_dev = data['Close'].std()
    variance = data['Close'].var()

    #Price chart
    price_chart = go.Figure()
    price_chart.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    price_chart.add_trace(go.Scatter(x=data.index, y=data['50-day MA'], mode='lines', name='50-day MA'))
    price_chart.add_trace(go.Scatter(x=data.index, y=data['200-day MA'], mode='lines', name='200-day MA'))
    price_chart.update_layout(title=f'{selected_stock} Prices and Moving Averages', xaxis_title='Date', yaxis_title='Price')

    #Volume chart
    volume_chart = px.histogram(data, x=data.index, y='Volume', nbins=50, title=f'{selected_stock} Trading Volume')
    volume_chart.update_layout(bargap=0.2)
    
    # Create RSI chart
    rsi_chart = go.Figure()
    rsi_chart.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'))
    rsi_chart.update_layout(title=f'{selected_stock} Relative Strength Index (RSI)', xaxis_title='Date', yaxis_title='RSI')

    # Create MACD chart
    macd_chart = go.Figure()
    macd_chart.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD'))
    macd_chart.add_trace(go.Scatter(x=data.index, y=data['MACD Signal'], mode='lines', name='MACD Signal'))
    macd_chart.add_trace(go.Bar(x=data.index, y=data['MACD Diff'], name='MACD Diff'))
    macd_chart.update_layout(title=f'{selected_stock} Moving Average Convergence Divergence (MACD)', xaxis_title='Date', yaxis_title='MACD')

    #Volatility scatter plot
    volatility_data = pd.DataFrame({'Stock': [selected_stock], 'Standard Deviation': [std_dev], 'Variance': [variance]})
    volatility_scatter = px.scatter(volatility_data, x='Standard Deviation', y='Variance', text='Stock', title='Volatility Assessment')
    volatility_scatter.update_traces(marker=dict(size=10, opacity=0.8), textposition='top center')

    # Display charts
    st.plotly_chart(price_chart)
    st.plotly_chart(volume_chart)
    st.plotly_chart(rsi_chart)
    st.plotly_chart(macd_chart)
    st.plotly_chart(volatility_scatter)