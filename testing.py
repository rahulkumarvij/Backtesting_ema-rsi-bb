import pandas as pd
import numpy as np

# Load the historical data
data = pd.read_csv("NIFTY 50_Data.csv")

# Calculate the EMA
data["ema_fast"] = data["close"].ewm(span=12, adjust=False).mean()
data["ema_slow"] = data["close"].ewm(span=26, adjust=False).mean()

# Calculate the RSI
delta = data["close"].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()
rs = avg_gain / avg_loss
data["rsi"] = 100 - (100 / (1 + rs))

# Calculate the Bollinger Bands
data["rolling_mean"] = data["close"].rolling(window=20).mean()
data["std"] = data["close"].rolling(window=20).std()
data["upper"] = data["rolling_mean"] + 2*data["std"]
data["lower"] = data["rolling_mean"] - 2*data["std"]

# Initialize the strategy variables
data["signal"] = 0
data["position"] = 0
data["profit"] = 0

# Backtesting loop
for i in range(1, len(data)):
    # EMA crossover strategy
    if data["ema_fast"][i] > data["ema_slow"][i] and data["ema_fast"][i-1] <= data["ema_slow"][i-1] and data["rsi"][i] > 50 and data["close"][i] < data["rolling_mean"][i]:
        data.at[i, "signal"] = 1
    elif data["ema_fast"][i] < data["ema_slow"][i] and data["ema_fast"][i-1] >= data["ema_slow"][i-1] and data["rsi"][i] < 50 and data["close"][i] > data["rolling_mean"][i]:
        data.at[i, "signal"] = -1

 
    # Update the position and profit based on the signal 
    if data["signal"][i] == 1 and data["position"][i-1] <= 0: 
        data.at[i, "position"] = 1 
        data.at[i, "profit"] = data["close"][i] - data["close"][i-1] 
    elif data["signal"][i] == -1 and data["position"][i-1] >= 0: 
        data.at[i, "position"] = -1 
        data.at[i, "profit"] = data["close"][i-1] - data["close"][i] 
    else: 
        data.at[i, "position"] = data["position"][i-1] 
        data.at[i, "profit"] = data["profit"][i-1] 
 
# Print the backtesting results 
print(data["profit"].sum()) 
