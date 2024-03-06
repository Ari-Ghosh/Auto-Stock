# Importing the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import floor
from termcolor import colored as cl

from data_extraction import get_historical_data
from macd_plot import plot_macd
from stochastoc_oscillator import get_stoch_osc
from macd_calculation import get_macd
from trading_strategy import trading_strategy



traindf, validationdf, testdf = get_historical_data('^NSEI')

print(traindf)



traindf['%k'], traindf['%d'] = get_stoch_osc(traindf['High'], traindf['Low'], traindf['Close'], 14, 3)
validationdf['%k'], validationdf['%d'] = get_stoch_osc(validationdf['High'], validationdf['Low'], validationdf['Close'], 14, 3)
testdf['%k'], testdf['%d'] = get_stoch_osc(testdf['High'], testdf['Low'], testdf['Close'], 14, 3)

print(traindf)
print(validationdf)
print(testdf)



traindf['macd'] = get_macd(traindf['Close'], 26, 12, 9)[0]
traindf['macd_signal'] = get_macd(traindf['Close'], 26, 12, 9)[1]
traindf['macd_hist'] = get_macd(traindf['Close'], 26, 12, 9)[2]
traindf = traindf.dropna()

validationdf['macd'] = get_macd(validationdf['Close'], 26, 12, 9)[0]
validationdf['macd_signal'] = get_macd(validationdf['Close'], 26, 12, 9)[1]
validationdf['macd_hist'] = get_macd(validationdf['Close'], 26, 12, 9)[2]
validationdf = validationdf.dropna()

testdf['macd'] = get_macd(testdf['Close'], 26, 12, 9)[0]
testdf['macd_signal'] = get_macd(testdf['Close'], 26, 12, 9)[1]
testdf['macd_hist'] = get_macd(testdf['Close'], 26, 12, 9)[2]
testdf = testdf.dropna()



plot_macd(traindf['Close'], traindf['macd'], traindf['macd_signal'], traindf['macd_hist'])



trading_strategy(testdf)