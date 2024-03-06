import pandas as pd
import matplotlib.pyplot as plt

def plot_trade(price, macd, macd_signal, hist, buy_price, sell_price):
    ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan = 5, colspan = 1)

    ax1.plot(price, color = 'skyblue', linewidth = 2, label = 'GOOGL')
    ax1.plot(googl.index, buy_price, marker = '^', color = 'green', markersize = 10, label = 'BUY SIGNAL', linewidth = 0)
    ax1.plot(googl.index, sell_price, marker = 'v', color = 'r', markersize = 10, label = 'SELL SIGNAL', linewidth = 0)
    ax1.legend()
    ax1.set_title('GOOGL MACD SIGNALS')
    ax2.plot(macd, color = 'grey', linewidth = 1.5, label = 'MACD')
    ax2.plot(macd_signal, color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

    for i in range(len(googl_macd)):
        if str(hist[i])[0] == '-':
            ax2.bar(googl_macd.index[i], hist[i], color = '#ef5350')
        else:
            ax2.bar(googl_macd.index[i], hist[i], color = '#26a69a')

    plt.legend(loc = 'lower right')
    plt.show()