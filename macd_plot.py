import matplotlib.pyplot as plt

# Plot styles
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

def plot_macd(prices, macd, signal, hist):
    ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan=5, colspan=1)

    ax1.plot(prices, linewidth=2.5)
    ax1.set_title('STOCK PRICES')
    ax2.plot(macd, color='grey', linewidth=1.5, label='MACD')
    ax2.plot(signal, color='skyblue', linewidth=1.5, label='SIGNAL')
    ax2.set_title('MACD Plottings')

    for i in range(len(prices)):
        if str(hist[i])[0] == '-':
            ax2.bar(prices.index[i], hist[i], color='#ef5350')
        else:
            ax2.bar(prices.index[i], hist[i], color='#26a69a')

    plt.legend(loc='lower right')
