import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def simulate_bitcoin_prices(days=60, initial_price=60000, mu=0.001, sigma=0.04):
    """
    Simulate Bitcoin prices using Geometric Brownian Motion (GBM).
    """
    np.random.seed(0) # Use a seed so the output is consistent
    prices = [initial_price]
    for _ in range(1, days):
        # GBM formula
        shock = np.random.normal(0, 1)
        price = prices[-1] * np.exp((mu - 0.5 * sigma**2) + sigma * shock)
        prices.append(price)

    dates = [datetime.today().date() - timedelta(days=days-i-1) for i in range(days)]

    df = pd.DataFrame({'Date': dates, 'Price': prices})
    df.set_index('Date', inplace=True)
    return df

def calculate_moving_averages(df):
    """
    Calculate 7-day and 30-day moving averages.
    """
    df['MA7'] = df['Price'].rolling(window=7).mean()
    df['MA30'] = df['Price'].rolling(window=30).mean()
    return df

def run_trading_algorithm(df, initial_balance=10000):
    """
    Implements a Golden Cross trading algorithm.
    Buys when 7-day MA crosses above 30-day MA.
    Sells when 7-day MA crosses below 30-day MA.
    """
    balance = initial_balance
    btc_held = 0
    position = 0 # 0 for no position, 1 for long

    print("=== Daily Ledger ===")

    for index, row in df.iterrows():
        price = row['Price']
        ma7 = row['MA7']
        ma30 = row['MA30']

        date_str = index.strftime('%Y-%m-%d')

        # Check if moving averages are available
        if pd.isna(ma7) or pd.isna(ma30):
            print(f"{date_str}: Hold (Not enough data) - Price: ${price:.2f}")
            continue

        action = "Hold"

        if ma7 > ma30 and position == 0:
            # Buy
            btc_held = balance / price
            balance = 0
            position = 1
            action = f"Buy {btc_held:.6f} BTC"
        elif ma7 < ma30 and position == 1:
            # Sell
            balance = btc_held * price
            btc_held = 0
            position = 0
            action = f"Sell for ${balance:.2f}"

        print(f"{date_str}: {action:<20} - Price: ${price:.2f} | MA7: ${ma7:.2f} | MA30: ${ma30:.2f}")

    # Calculate final portfolio value
    final_value = balance + (btc_held * df.iloc[-1]['Price'])

    print("\n=== Final Portfolio Performance ===")
    print(f"Initial Balance: ${initial_balance:.2f}")
    print(f"Final Portfolio: ${final_value:.2f}")
    print(f"Return:          {((final_value - initial_balance) / initial_balance * 100):.2f}%")

if __name__ == "__main__":
    print("Simulating Bitcoin Prices...")
    df = simulate_bitcoin_prices(days=60)
    df = calculate_moving_averages(df)
    run_trading_algorithm(df)
