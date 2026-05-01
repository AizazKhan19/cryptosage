import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

# RSI Calculation
def calulate_rsi(close_prices):
    """
    Calculate the Relative Strength Index (RSI) for a given list of closing prices.

    """

    # convet list to dataframe
    df = pd.DataFrame(close_prices, columns=['close'])

    # calculate RSI 
    rsi = RSIIndicator(df['close'], window = 14)
    df['RSI'] = rsi.rsi()

    # return latest RSI value
    return df['RSI'].iloc[-1]

# MACD Calculation
def calculate_macd(close_prices):
    """
    Calculate MACD indicator
    
    Rerurns : MACD line value, Signal line value, and decision

    """
    # convert closing prices to dataframe
    df = pd.DataFrame(close_prices, columns=['close'])

    # calculate MACD
    macd = MACD(close =  df['close'])
    df['macd'] =  macd.macd()
    df['signal'] = macd.macd_signal()

    # get latest values
    macd_values = df['macd'].iloc[-1]
    signal_values = df['signal'].iloc[-1]

    # determine buy/sell signal
    if macd_values > signal_values:
        decision = "Bullish (BUY)"
    elif macd_values < signal_values:
        decision = "Bearish (SELL)"
    else:
        decision = "Neutral (WAIT)"
    
    return macd_values, signal_values, decision
