import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from math import floor
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

stock_symbol = "^NSEI"

base_slow = 26
base_fast = 12
base_smooth = 9

slow_range = range(10, 31, 2)
fast_range = range(5, 21, 2)
smooth_range = range(5, 16, 2)

param_grid = pd.DataFrame([(slow, fast, smooth) for slow in slow_range for fast in fast_range for smooth in smooth_range],
                          columns=['slow', 'fast', 'smooth'])

def get_macd(price, slow, fast, smooth):
    exp1 = price.ewm(span=fast, adjust=False).mean()
    exp2 = price.ewm(span=slow, adjust=False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns={'Close': 'macd'})
    signal = pd.DataFrame(macd.ewm(span=smooth, adjust=False).mean()).rename(columns={'macd': 'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns={0: 'hist'})
    return macd, signal, hist

def get_historical_data(symbol):
    df = yf.Ticker(symbol)
    df = df.history(period="max")
    del df["Dividends"]
    del df["Stock Splits"]

    traindf = df[df.index < "2021-01-01"]
    traindf = traindf[traindf.index >= "2015-01-01"]
    validationdf = df[df.index < "2023-01-01"]
    validationdf = validationdf[validationdf.index >= "2021-01-01"]
    testdf = df[df.index >= "2023-01-01"]

    return traindf, validationdf, testdf