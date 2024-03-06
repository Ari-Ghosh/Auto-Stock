import yfinance as yf
import pandas as pd
import numpy as np

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