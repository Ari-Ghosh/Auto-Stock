# Importing the libraries
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from math import floor
from termcolor import colored as cl

# Plot styles
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

# Extracting stock data
def get_historical_data(symbol):
    df = yf.Ticker(symbol)
    df = df.history(period="max")
    print(df)
    print(df.index)
    del df["Dividends"] 
    del df["Stock Splits"]
    print(df)
    
    traindf = df[df.index < "2021-01-01"]
    validationdf = df[df.index < "2023-01-01"]
    validationdf = validationdf[validationdf.index >= "2021-01-01"] 
    testdf = df[df.index >= "2023-01-01"]
    print(traindf)
    print(validationdf)
    print(testdf)

    return traindf, validationdf, testdf

traindf, validationdf, testdf = get_historical_data('^NSEI')

print(traindf['High'])

# Stochastic Oscillator Calculation
def get_stoch_osc(high, low, close, k_lookback, d_lookback):
    lowest_low = low.rolling(k_lookback).min()
    highest_high = high.rolling(k_lookback).max()
    k_line = ((close - lowest_low) / (highest_high - lowest_low)) * 100
    d_line = k_line.rolling(d_lookback).mean()
    return k_line, d_line

traindf['%k'], traindf['%d'] = get_stoch_osc(traindf['High'], traindf['Low'], traindf['Close'], 14, 3)

print(traindf)

# MACD Calculation
def get_macd(price, slow, fast, smooth):
    exp1 = price.ewm(span = fast, adjust = False).mean()
    exp2 = price.ewm(span = slow, adjust = False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns = {'close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    return macd, signal, hist

traindf['macd'] = get_macd(traindf['close'], 26, 12, 9)[0]
traindf['macd_signal'] = get_macd(traindf['close'], 26, 12, 9)[1]
traindf['macd_hist'] = get_macd(traindf['close'], 26, 12, 9)[2]
traindf = traindf.dropna()

# # MACD plot
# def plot_macd(prices, macd, signal, hist):
#     ax1 = plt.subplot2grid((11,1), (0,0), rowspan = 5, colspan = 1)
#     ax2 = plt.subplot2grid((11,1), (6,0), rowspan = 5, colspan = 1)

#     ax1.plot(prices, linewidth = 2.5)
#     ax1.set_title('AAPL STOCK PRICES')
#     ax2.plot(macd, color = 'grey', linewidth = 1.5, label = 'MACD')
#     ax2.plot(signal, color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')
#     ax2.set_title('AAPL MACD 26,12,9')

#     for i in range(len(prices)):
#         if str(hist[i])[0] == '-':
#             ax2.bar(prices.index[i], hist[i], color = '#ef5350')
#         else:
#             ax2.bar(prices.index[i], hist[i], color = '#26a69a')

#     plt.legend(loc = 'lower right')

# plot_macd(traindf['close'], traindf['macd'], traindf['macd_signal'], traindf['macd_hist'])

# # Trading Strategy
# def implement_stoch_macd_strategy(prices, k, d, macd, macd_signal):    
#     buy_price = []
#     sell_price = []
#     stoch_macd_signal = []
#     signal = 0

#     for i in range(len(prices)):
#         if k[i] < 30 and d[i] < 30 and macd[i] < -2 and macd_signal[i] < -2:
#             if signal != 1:
#                 buy_price.append(prices[i])
#                 sell_price.append(np.nan)
#                 signal = 1
#                 stoch_macd_signal.append(signal)
#             else:
#                 buy_price.append(np.nan)
#                 sell_price.append(np.nan)
#                 stoch_macd_signal.append(0)
                
#         elif k[i] > 70 and d[i] > 70 and macd[i] > 2 and macd_signal[i] > 2:
#             if signal != -1 and signal != 0:
#                 buy_price.append(np.nan)
#                 sell_price.append(prices[i])
#                 signal = -1
#                 stoch_macd_signal.append(signal)
#             else:
#                 buy_price.append(np.nan)
#                 sell_price.append(np.nan)
#                 stoch_macd_signal.append(0)
        
#         else:
#             buy_price.append(np.nan)
#             sell_price.append(np.nan)
#             stoch_macd_signal.append(0)
            
#     return buy_price, sell_price, stoch_macd_signal
            
# buy_price, sell_price, stoch_macd_signal = implement_stoch_macd_strategy(traindf['close'], traindf['%k'], traindf['%d'], traindf['macd'], traindf['macd_signal'])

# position = []
# for i in range(len(stoch_macd_signal)):
#     if stoch_macd_signal[i] > 1:
#         position.append(0)
#     else:
#         position.append(1)
        
# for i in range(len(traindf['close'])):
#     if stoch_macd_signal[i] == 1:
#         position[i] = 1
#     elif stoch_macd_signal[i] == -1:
#         position[i] = 0
#     else:
#         position[i] = position[i-1]
        
# # Position
# close_price = traindf['close']
# k_line = traindf['%k']
# d_line = traindf['%d']
# macd_line = traindf['macd']
# signal_line = traindf['macd_signal']
# stoch_macd_signal = pd.DataFrame(stoch_macd_signal).rename(columns = {0:'stoch_macd_signal'}).set_index(traindf.index)
# position = pd.DataFrame(position).rename(columns = {0:'stoch_macd_position'}).set_index(traindf.index)

# frames = [close_price, k_line, d_line, macd_line, signal_line, stoch_macd_signal, position]
# strategy = pd.concat(frames, join = 'inner', axis = 1)

# strategy.head()

# rets = traindf.close.pct_change().dropna()
# strat_rets = strategy.stoch_macd_position[1:]*rets

# plt.title('Daily Returns')
# rets.plot(color = 'blue', alpha = 0.3, linewidth = 7)
# strat_rets.plot(color = 'r', linewidth = 1)
# plt.show()

# rets_cum = (1 + rets).cumprod() - 1 
# strat_cum = (1 + strat_rets).cumprod() - 1

# plt.title('Cumulative Returns')
# rets_cum.plot(color = 'blue', alpha = 0.3, linewidth = 7)
# strat_cum.plot(color = 'r', linewidth = 2)
# plt.show()