import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def macd_trading_strategy(prices, k, d, macd, macd_signal):
        buy_price = []
        sell_price = []
        stoch_macd_signal = []
        signal = 0

        for i in range(len(prices)):
            if k[i] < 30 and d[i] < 30 and macd[i] < -2 and macd_signal[i] < -2:
                if signal != 1:
                    buy_price.append(prices[i])
                    sell_price.append(np.nan)
                    signal = 1
                    stoch_macd_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    stoch_macd_signal.append(0)

            elif k[i] > 70 and d[i] > 70 and macd[i] > 2 and macd_signal[i] > 2:
                if signal != -1 and signal != 0:
                    buy_price.append(np.nan)
                    sell_price.append(prices[i])
                    signal = -1
                    stoch_macd_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    stoch_macd_signal.append(0)

            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                stoch_macd_signal.append(0)

        return buy_price, sell_price, stoch_macd_signal