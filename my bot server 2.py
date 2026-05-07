# COMPLET PASS - Updated with SL set at order execution STARTED
import MetaTrader5 as mt5
import pandas as pd
import logging
import time
from datetime import datetime, timezone
import MetaTrader5 as mt5
print(mt5.__version__)

# Configure logging
logging.basicConfig(
    filename='eurusd_trade_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Login credentials
ACCOUNT = 423342311
PASSWORD = "*******"
SERVER = "Exn*******"

# Connect to MT5
if not mt5.initialize():
    logging.error(f"MetaTrader5 initialization failed: {mt5.last_error()}")
    print("MetaTrader5 initialization failed.")
    quit()

# Login to account
if not mt5.login(ACCOUNT, password=PASSWORD, server=SERVER):
    logging.error(f"Login failed: {mt5.last_error()}")
    print("Login failed. Check your credentials.")
    mt5.shutdown()
    quit()

print(f"Logged in to account #{ACCOUNT}")
logging.info(f"Logged in to account #{ACCOUNT}")

# Constants
SYMBOL = "EURUSDm"
TIMEFRAME_M5 = mt5.TIMEFRAME_M5
TIMEFRAME_M1 = mt5.TIMEFRAME_M1  # For SMA filter
RISK_PERCENT = 0.0025
TP_PIPS = 0.0004  # 0.8 pips
SL_PIPS = 0.0002   # 0.4 pips
MAGIC_NUMBER = 234000

# Stochastic parameters
STOCHASTIC_PERIOD = 14
STOCHASTIC_SLOWING = 3
STOCHASTIC_MA_PERIOD = 3

# SMA parameters
SMA_FAST_PERIOD = 10
SMA_SLOW_PERIOD = 20

# Trackers
last_traded_candle_time = None
active_trade = False
last_exit_candle_time = None  # Track when position was exited

def fetch_completed_candle(symbol, timeframe):
    """Fetches the last completed candle with validation"""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 1, 1)
    if rates is None or len(rates) == 0:
        print("Failed to fetch rates or empty response")
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s').dt.tz_localize('UTC')
    return df.iloc[0]

def get_stochastic(symbol, timeframe, count=50):
    """Calculates Stochastic Oscillator values"""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count + STOCHASTIC_PERIOD + STOCHASTIC_SLOWING)
    if rates is None or len(rates) < STOCHASTIC_PERIOD + STOCHASTIC_SLOWING:
        print("Failed to fetch rates for Stochastic calculation")
        return None, None
    
    df = pd.DataFrame(rates)
    
    # Calculate Stochastic
    low_min = df['low'].rolling(STOCHASTIC_PERIOD).min()
    high_max = df['high'].rolling(STOCHASTIC_PERIOD).max()
    
    k = 100 * ((df['close'] - low_min) / (high_max - low_min))
    k = k.rolling(STOCHASTIC_SLOWING).mean()  # %K line
    d = k.rolling(STOCHASTIC_MA_PERIOD).mean()  # %D line
    
    return k.iloc[-1], d.iloc[-1]

def get_sma_values(symbol, timeframe, fast_period, slow_period):
    """Gets SMA values for filtering"""
    # We need enough bars to calculate both SMAs
    needed_bars = max(fast_period, slow_period) + 10
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, needed_bars)
    if rates is None or len(rates) < needed_bars:
        print("Failed to fetch rates for SMA calculation")
        return None, None
    
    df = pd.DataFrame(rates)
    sma_fast = df['close'].rolling(fast_period).mean().iloc[-1]
    sma_slow = df['close'].rolling(slow_period).mean().iloc[-1]
    
    return sma_fast, sma_slow

def get_valid_volume(symbol, calculated_volume):
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print("Failed to get symbol info for volume validation")
        return 0.0
    
    volume_min = symbol_info.volume_min
    volume_max = symbol_info.volume_max
    volume_step = symbol_info.volume_step

    valid_volume = max(volume_min, min(volume_max, calculated_volume))
    valid_volume = round(valid_volume / volume_step) * volume_step
    return valid_volume

def calculate_position_size(balance, entry_price, sl_price):
    risk_amount = balance * RISK_PERCENT
    price_diff = abs(entry_price - sl_price)
    if price_diff == 0:
        print("Zero price difference between entry and SL")
        return 0.0
    
    point_value = 10  # $10 per 0.0001
    pips = price_diff / 0.0001
    position_size = (risk_amount / (pips * point_value)) 
    return position_size

def place_order(symbol, trade_type, lot, entry_price, tp_price, sl_price):
    global active_trade
    valid_lot = get_valid_volume(symbol, lot)
    if valid_lot <= 0:
        print(f"Invalid lot size: {lot} -> {valid_lot}")
        return

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print("Failed to get symbol info for order placement")
        return

    digits = symbol_info.digits
    entry_price = round(entry_price, digits)
    tp_price = round(tp_price, digits)
    sl_price = round(sl_price, digits)
    print(f"Placing {trade_type} order: Entry={entry_price:.5f}, SL={sl_price:.5f}, TP={tp_price:.5f}, Lots={valid_lot}")

    order_type = mt5.ORDER_TYPE_BUY if trade_type == "Long" else mt5.ORDER_TYPE_SELL
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": valid_lot,
        "type": order_type,
        "price": entry_price,
        "sl": sl_price,
        "tp": tp_price,
        "deviation": 10,
        "magic": MAGIC_NUMBER,
        "comment": f"{trade_type} trade",
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        error_msg = f"Order failed: {result.comment} (Error code: {result.retcode})"
        print(error_msg)
        logging.error(error_msg)
    else:
        success_msg = f"Order executed: {trade_type} {valid_lot} lots @ {entry_price:.5f}"
        print(success_msg)
        logging.info(success_msg)
        active_trade = True

# Main trading loop
print("Starting trading loop...")
while True:
    try:
        # Check for active positions and update status
        positions = mt5.positions_get(symbol=SYMBOL, magic=MAGIC_NUMBER)
        
        # Check if position was just closed
        if active_trade and len(positions) == 0:
            last_exit_candle_time = fetch_completed_candle(SYMBOL, TIMEFRAME_M5)['time']
            print(f"Position closed on candle: {last_exit_candle_time}")
        
        active_trade = len(positions) > 0

        # Skip if active trade exists
        if active_trade:
            time.sleep(0.1)
            continue

        # Get last COMPLETED 5-minute candle
        completed_candle = fetch_completed_candle(SYMBOL, TIMEFRAME_M5)
        if completed_candle is None:
            time.sleep(1)
            continue

        # Check if we've already processed this candle
        if last_traded_candle_time == completed_candle['time']:
            time.sleep(0.1)
            continue

        # Check if this is the same candle where position was exited
        if last_exit_candle_time == completed_candle['time']:
            print(f"Skipping trade on candle where position was exited: {completed_candle['time']}")
            time.sleep(0.1)
            continue

        print(f"\nCompleted 5M Candle: {completed_candle['time']}")
        print(f"High: {completed_candle['high']:.5f} | Low: {completed_candle['low']:.5f}")

        # Get current tick
        tick = mt5.symbol_info_tick(SYMBOL)
        if not tick:
            time.sleep(0.1)
            continue

        # Get Stochastic values
        k, d = get_stochastic(SYMBOL, TIMEFRAME_M5)
        if k is None or d is None:
            time.sleep(0.1)
            continue
            
        print(f"Stochastic: K={k:.2f}, D={d:.2f}")

        # Get SMA values for filtering (1-minute timeframe)
        sma_fast, sma_slow = get_sma_values(SYMBOL, TIMEFRAME_M1, SMA_FAST_PERIOD, SMA_SLOW_PERIOD)
        if sma_fast is None or sma_slow is None:
            time.sleep(0.1)
            continue
            
        print(f"SMA Filter: Fast={sma_fast:.5f}, Slow={sma_slow:.5f}")

        # === SWAPPED LOGIC START ===
        entry_type = None
        if (tick.ask > completed_candle['high'] and k > d and sma_fast > sma_slow):
            entry_type = "Short"  # Swapped from "Long"
            entry_price = tick.ask
            tp_price = entry_price - TP_PIPS
            sl_price = entry_price + SL_PIPS
            print(f"Short trigger (Swapped): {tick.ask:.5f} > {completed_candle['high']:.5f}, K > D, and SMA10 > SMA20")
        elif (tick.bid < completed_candle['low'] and k < d and sma_fast < sma_slow):
            entry_type = "Long"  # Swapped from "Short"
            entry_price = tick.bid
            tp_price = entry_price + TP_PIPS
            sl_price = entry_price - SL_PIPS
            print(f"Long trigger (Swapped): {tick.bid:.5f} < {completed_candle['low']:.5f}, K < D, and SMA10 < SMA20")
        # === SWAPPED LOGIC END ===

        if entry_type:
            account_info = mt5.account_info()
            if not account_info:
                continue
                
            balance = account_info.balance
            
            # Calculate position size
            position_size = calculate_position_size(balance, entry_price, sl_price)
            valid_lot = get_valid_volume(SYMBOL, position_size)
            
            if valid_lot > 0:
                print(f"Position size: {valid_lot} lots | Risk: {RISK_PERCENT*100}%")
                place_order(SYMBOL, entry_type, valid_lot, entry_price, tp_price, sl_price)
                last_traded_candle_time = completed_candle['time']
            else:
                print("Invalid position size - trade skipped")

        time.sleep(0.1)

    except Exception as e:
        logging.error(f"Error in main loop: {str(e)}")
        print(f"Error occurred: {str(e)}")
        time.sleep(0.1)

mt5.shutdown()
