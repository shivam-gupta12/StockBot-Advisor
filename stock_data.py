
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def fetch_stock_data(ticker , period = "1y"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)  
    return hist[['Close']] 

def calculate_moving_averages(data, window_sizes):
    for window in window_sizes:
        data[f'MA_{window}'] = data['Close'].rolling(window=window).mean()
    return data

def plot_stock_trends(data, ticker):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Closing Prices', color='blue')
    for col in data.columns[1:]:
        plt.plot(data[col], label=col)
    plt.title(f'Trend Analysis for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

tsla_data = fetch_stock_data("TSLA")

tsla_data = calculate_moving_averages(tsla_data, [20, 50, 100])  
tsla_data.to_csv('TSLA_Stock_Data.csv')
plot_stock_trends(tsla_data, "TSLA")

