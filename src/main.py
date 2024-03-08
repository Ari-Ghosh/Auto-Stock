from data_extraction import get_historical_data
from macd_plot import plot_macd
from stochastoc_oscillator import get_stoch_osc
from macd_calculation import get_macd
from trading_strategy import macd_trading_strategy
from trading_list_plot import plot_trade

stock_symbol = '^NSEI'
slow = 26
fast = 12
smooth = 9

# PARAMETER GRID
slow_range = range(10, 31, 2)
fast_range = range(5, 21, 2)
smooth_range = range(5, 16, 2)


traindf, validationdf, testdf = get_historical_data(stock_symbol)
print(traindf)
print(validationdf)
print(testdf)



traindf['%k'], traindf['%d'] = get_stoch_osc(traindf['High'], traindf['Low'], traindf['Close'], 14, 3)
validationdf['%k'], validationdf['%d'] = get_stoch_osc(validationdf['High'], validationdf['Low'], validationdf['Close'], 14, 3)
testdf['%k'], testdf['%d'] = get_stoch_osc(testdf['High'], testdf['Low'], testdf['Close'], 14, 3)

print(traindf)
print(validationdf)
print(testdf)


traindf = get_macd(traindf['Close'], slow, fast, smooth)
traindf = traindf.dropna()

validationdf = get_macd(validationdf['Close'], slow, fast, smooth)
validationdf = validationdf.dropna()

testdf = get_macd(testdf['Close'], slow, fast, smooth)
testdf = testdf.dropna()

print(traindf)
print(validationdf)
print(testdf)



# plot_macd(traindf['Close'], traindf['macd'], traindf['signal'], traindf['hist'])



# buy_price, sell_price, macd_signal = macd_trading_strategy(testdf['Close'], testdf['%k'], testdf['%d'], testdf['macd'], testdf['signal'])

# plot_trade(testdf['Close'], testdf['macd'], testdf['macd_signal'], testdf['macd_hist'], buy_price, sell_price)