import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from math import floor

def get_historical_data(symbol):
    """
    Retrieves historical stock data from Yahoo Finance.

    Args:
    - symbol (str): Stock symbol.

    Returns:
    - traindf, validationdf, testdf (pd.DataFrame): Dataframes for training, validation, and testing periods.
    """
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="max")
    history = history.drop(columns=["Dividends", "Stock Splits"])

    traindf = history[(history.index >= "2015-01-01") & (history.index < "2021-01-01")]
    validationdf = history[(history.index >= "2021-01-01") & (history.index < "2023-01-01")]
    testdf = history[history.index >= "2023-01-01"]

    return traindf, validationdf, testdf

def calculate_macd(price, slow, fast, smooth):
    """
    Calculates MACD indicators.

    Args:
    - price (pd.Series): Price data.
    - slow (int): Slow moving average period.
    - fast (int): Fast moving average period.
    - smooth (int): Smoothing period.

    Returns:
    - macd_df (pd.DataFrame): DataFrame containing MACD, Signal, and Histogram.
    """
    exp1 = price.ewm(span=fast, adjust=False).mean()
    exp2 = price.ewm(span=slow, adjust=False).mean()

    macd = exp1 - exp2
    signal = macd.ewm(span=smooth, adjust=False).mean()
    hist = macd - signal

    macd_df = pd.DataFrame({"MACD": macd, "Signal": signal, "Histogram": hist})
    return macd_df

def implement_macd_strategy(prices, macd_data):
    """
    Implements MACD strategy.

    Args:
    - prices (pd.Series): Price data.
    - macd_data (pd.DataFrame): DataFrame containing MACD, Signal, and Histogram.

    Returns:
    - buy_price, sell_price, macd_signal (list): Lists indicating buy and sell prices, and MACD signals.
    """
    buy_price = []
    sell_price = []
    macd_signal = []
    signal = 0

    for i in range(len(macd_data)):
        if macd_data['MACD'][i] > macd_data['Signal'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        elif macd_data['MACD'][i] < macd_data['Signal'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            macd_signal.append(0)

    return buy_price, sell_price, macd_signal

def plot_macd_indicator(stock_data, macd_data):
    """
    Plots MACD indicator.

    Args:
    - stock_data (pd.DataFrame): DataFrame containing stock data.
    - macd_data (pd.DataFrame): DataFrame containing MACD, Signal, and Histogram.

    Returns:
    - None
    """
    buy_price, sell_price, _ = implement_macd_strategy(stock_data['Close'], macd_data)

    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(stock_data['Close'], color='skyblue', linewidth=2, label=STOCK_SYMBOL)
    plt.plot(stock_data.index, buy_price, marker='^', color='green', markersize=10, label='BUY SIGNAL', linewidth=0)
    plt.plot(stock_data.index, sell_price, marker='v', color='r', markersize=10, label='SELL SIGNAL', linewidth=0)
    plt.legend()
    plt.title('MACD SIGNALS')

    plt.subplot(2, 1, 2)
    plt.plot(macd_data['MACD'], color='grey', linewidth=1.5, label='MACD')
    plt.plot(macd_data['Signal'], color='skyblue', linewidth=1.5, label='SIGNAL')
    plt.bar(macd_data.index, macd_data['Histogram'], color=np.where(macd_data['Histogram'] < 0, 'red', 'green'))
    plt.legend(loc='lower right')
    plt.show()

def create_position(macd_signal, train_data, macd_data):
    """
    Creates positions in the market based on MACD signals.

    Args:
    - macd_signal (list): List of MACD signals.
    - train_data (pd.DataFrame): DataFrame containing training data.
    - macd_data (pd.DataFrame): DataFrame containing MACD, Signal, and Histogram.

    Returns:
    - strategy (pd.DataFrame): DataFrame containing strategy information.
    """
    position = [1 if sig > 0 else 0 for sig in macd_signal]

    for i in range(len(train_data['Close'])):
        if macd_signal[i] == 1:
            position[i] = 1
        elif macd_signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i-1]

    macd_signal_df = pd.DataFrame(macd_signal, columns=['macd_signal'], index=train_data.index)
    position_df = pd.DataFrame(position, columns=['macd_position'], index=train_data.index)
    
    strategy = pd.concat([train_data['Close'], macd_data['MACD'], macd_data['Signal'], macd_signal_df, position_df], axis=1)
    return strategy

def backtesting(strategy, train_data):
    """
    Performs backtesting to evaluate the MACD strategy.

    Args:
    - strategy (pd.DataFrame): DataFrame containing strategy information.
    - train_data (pd.DataFrame): DataFrame containing training data.

    Returns:
    - total_investment_ret (float): Total investment return.
    - profit_percentage (int): Profit percentage.
    """
    stock_returns = train_data['Close'].pct_change().shift(-1).fillna(0)
    strategy_returns = strategy['macd_position'].shift(1) * stock_returns
    total_investment_return = np.sum(strategy_returns)
    
    initial_investment = 100000
    final_investment_value = initial_investment * (1 + total_investment_return)
    profit_percentage = floor((final_investment_value - initial_investment) / initial_investment * 100)
    
    return final_investment_value, profit_percentage

def find_best_macd_parameters(param_grid, traindf):
    """
    Finds the best MACD parameters.

    Args:
    - param_grid (pd.DataFrame): DataFrame containing parameter grid.
    - traindf (pd.DataFrame): DataFrame containing training data.

    Returns:
    - best_params (tuple): Best MACD parameters.
    - max_profit (int): Maximum profit percentage.
    """
    best_params = None
    max_profit = -float('inf')
    
    for index, row in param_grid.iterrows():
        slow, fast, smooth = row['slow'], row['fast'], row['smooth']
        macd_df = calculate_macd(traindf['Close'], slow, fast, smooth)
        buy_price, sell_price, macd_signal = implement_macd_strategy(traindf['Close'], macd_df)
        strategy = create_position(macd_signal, traindf, macd_df)
        total_inv_ret, profit_per = backtesting(strategy, traindf)

        if profit_per > max_profit:
            max_profit = profit_per
            best_params = (slow, fast, smooth)

    return best_params, max_profit

def main():
    # Parameters
    STOCK_SYMBOL = input("Enter the Stock Signal: ")  # Symbol for the stock Ex: ^NSEI, TCS.NS, INFY.NS, etc.
    BASE_SLOW = 26
    BASE_FAST = 12
    BASE_SMOOTH = 9

    # Parameter Ranges
    SLOW_RANGE = range(7, 31, 1)
    FAST_RANGE = range(2, 25, 1)
    SMOOTH_RANGE = range(2, 18, 1)
    
    traindf, validationdf, testdf = get_historical_data(STOCK_SYMBOL)
    param_grid = pd.DataFrame([(slow, fast, smooth) for slow in SLOW_RANGE for fast in FAST_RANGE for smooth in SMOOTH_RANGE], columns=['slow', 'fast', 'smooth'])

    best_params, max_profit = find_best_macd_parameters(param_grid, traindf)
    print(f"Best MACD Parameters: slow={best_params[0]}, fast={best_params[1]}, smooth={best_params[2]}")
    print(f"Highest Profit Percentage: {max_profit}%")

if __name__ == "__main__":
    main()