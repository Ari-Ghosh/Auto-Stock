import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def trading_strategy(df):
    def implement_stoch_macd_strategy(prices, k, d, macd, macd_signal):
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

    buy_price, sell_price, stoch_macd_signal = implement_stoch_macd_strategy(df['Close'], df['%k'],
                                                                             df['%d'], df['macd'],
                                                                             df['macd_signal'])

    position = []
    for i in range(len(stoch_macd_signal)):
        if stoch_macd_signal[i] > 1:
            position.append(0)
        else:
            position.append(1)

    for i in range(len(df['Close'])):
        if stoch_macd_signal[i] == 1:
            position[i] = 1
        elif stoch_macd_signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i - 1]

    # Position
    close_price = df['Close']
    k_line = df['%k']
    d_line = df['%d']
    macd_line = df['macd']
    signal_line = df['macd_signal']
    stoch_macd_signal = pd.DataFrame(stoch_macd_signal).rename(columns={0: 'stoch_macd_signal'}).set_index(
        df.index)
    position = pd.DataFrame(position).rename(columns={0: 'stoch_macd_position'}).set_index(df.index)

    frames = [close_price, k_line, d_line, macd_line, signal_line, stoch_macd_signal, position]
    strategy = pd.concat(frames, join='inner', axis=1)

    strategy.head()

    rets = df.close.pct_change().dropna()
    strat_rets = strategy.stoch_macd_position[1:] * rets

    plt.title('Daily Returns')
    rets.plot(color='blue', alpha=0.3, linewidth=7)
    strat_rets.plot(color='r', linewidth=1)
    plt.show()

    rets_cum = (1 + rets).cumprod() - 1
    strat_cum = (1 + strat_rets).cumprod() - 1

    plt.title('Cumulative Returns')
    rets_cum.plot(color='blue', alpha=0.3, linewidth=7)
    strat_cum.plot(color='r', linewidth=2)
    plt.show()