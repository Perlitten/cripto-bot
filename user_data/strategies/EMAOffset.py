# --- Do not remove these libs ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IntParameter, IStrategy, merge_informative_pair)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib


class EMAOffset(IStrategy):
    """
    EMAOffset strategy - simple and efficient strategy for Kraken
    
    This strategy is designed to be lightweight and efficient, 
    using only essential indicators to make trading decisions.
    """
    
    INTERFACE_VERSION = 3
    
    # Buy hyperspace params:
    buy_params = {
        "ema_offset": 0.98,
        "rsi_buy": 30,
    }

    # Sell hyperspace params:
    sell_params = {
        "ema_offset_high": 1.02,
        "rsi_sell": 70,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.05,
        "30": 0.025,
        "60": 0.015,
        "120": 0.01,
        "240": 0.005,
        "1440": 0
    }

    # Stoploss:
    stoploss = -0.25

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.005
    trailing_stop_positive_offset = 0.025
    trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy
    timeframe = '15m'  # Increased from 5m to 15m for better performance

    # Run "populate_indicators" only for new candle.
    process_only_new_candles = True

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Optional order type mapping
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force
    order_time_in_force = {
        'entry': 'gtc',
        'exit': 'gtc'
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame
        
        Simplified version with minimal indicators for better performance
        """
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # EMA - Exponential Moving Average (only the essential ones)
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)

        # Volume Filter
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=30).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        """
        dataframe.loc[
            (
                # General market conditions filter
                (dataframe['ema50'] > dataframe['ema200']) &  # Uptrend
                
                # Entry conditions
                (dataframe['rsi'] < self.buy_params['rsi_buy']) &  # RSI oversold
                (dataframe['close'] < dataframe['ema50'] * self.buy_params['ema_offset']) &  # Price below EMA with offset
                (dataframe['volume'] > dataframe['volume_mean'] * 0.75)  # Volume check
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        """
        dataframe.loc[
            (
                # Exit conditions
                (dataframe['rsi'] > self.sell_params['rsi_sell']) &  # RSI overbought
                (dataframe['close'] > dataframe['ema50'] * self.sell_params['ema_offset_high']) &  # Price above EMA with offset
                (dataframe['volume'] > 0)  # Volume check
            ),
            'exit_long'] = 1

        return dataframe
