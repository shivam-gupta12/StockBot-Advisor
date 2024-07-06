import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

def fetch_stock_data(ticker , period = "1y"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)  
    return hist[['Close']] 

def calculate_moving_averages(data, window_sizes=[20,50,100]):
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
    
    # Create a BytesIO buffer to save image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')  # Save the figure in the buffer as PNG
    plt.close()  # Close the plot to free up memory

    # Encode the image in the buffer to Base64
    buffer.seek(0)  # Rewind the buffer to the beginning so we can read its content
    image_png = buffer.getvalue()  # Read the contents of the buffer
    base64_encoded = base64.b64encode(image_png)  # Encode these contents as Base64
    return base64_encoded.decode('utf-8')  # Convert byte stream to string

# tsla_data = fetch_stock_data("TSLA")

# tsla_data = calculate_moving_averages(tsla_data, [20, 50, 100])  
# tsla_data.to_csv('TSLA_Stock_Data.csv')
# plot_stock_trends(tsla_data, "TSLA")

